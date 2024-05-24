import typing
import logging


import telegram
import telegram.helpers
import langdetect # type: ignore
import google.cloud.translate
import google.api_core
import google.api_core.retry_async

from vladpy_telegram_ro_bot._application._translator._message_sentences_extractor import MessageSentencesExtractor
from vladpy_telegram_ro_bot._application._config._bot_config import BotConfig
from vladpy_telegram_ro_bot._application._defaults._gcloud_client_defaults import GCLoudClientDefaults


langdetect.DetectorFactory.seed = 0


# TODO fix: add Google Translate attribution


class Translator:


	def __init__(
			self,
			config: BotConfig,
			gcloud_credentials: typing.Any,
		) -> None:

		self.__logger = logging.getLogger('vladpy_telegram_ro_bot.Translator')

		self.__logger.info('init')

		self.__config = config
		self.__use_langdetect_f = False
		self.__use_gcloud_f = False

		# TODO improve: use process pool

		self.__message_senteces_extractor = MessageSentencesExtractor()

		self.__gtranslate_client = (
			google.cloud.translate.TranslationServiceAsyncClient(
				credentials=gcloud_credentials,
			)
		)

		self.set_use_langdetect_f(self.__config.use_langdetect_f)
		self.set_use_gcloud_f(self.__config.use_gcloud_f)


	def set_use_langdetect_f(
			self,
			use_langdetect_f: bool,
		) -> None:

		self.__use_langdetect_f = use_langdetect_f

		if self.__use_langdetect_f:
			self.__logger.info('use langdetect flag set')
		else:
			self.__logger.info('use langdetect flag unset')


	def set_use_gcloud_f(
			self,
			use_gcloud_f: bool,
		) -> None:

		self.__use_gcloud_f = use_gcloud_f

		if self.__use_gcloud_f:
			self.__logger.info('use gcloud flag set')
		else:
			self.__logger.info('use gcloud flag unset')


	async def translate(
			self,
			update_id: int,
			message: telegram.Message,
			language_code: typing.Optional[str],
			username: str,
		) -> typing.Optional[str]:

		self.__logger.info('translate begin [%s]', update_id)

		if (
				sum((
					(message.text is not None and len(message.text) > 0),
					(message.caption is not None and len(message.caption) > 0),
				))
				> 1
			):

			self.__logger.warning('translate [%s], text ambiguity', update_id)

		message_text = message.text or message.caption

		if message_text is None:
			self.__logger.warning('translate end [%s], no text', update_id)
			return None

		message_target_language_detect_f = False

		if self.__use_langdetect_f:

			message_target_language_detect_f = (
				self.__detect_target_language(
					message_text=message_text,
					language_code='ro',
				)
			)

		if (
				not message_target_language_detect_f
				and not self.__use_langdetect_f
			):

			self.__logger.info('translate end [%s], no target language', update_id)
			return None

		message_entities_dict: dict[telegram.MessageEntity, str] = dict()

		if message.text is not None and len(message.text) > 0:
			message_entities_dict = message.parse_entities()

		elif message.caption is not None and len(message.caption) > 0:
			message_entities_dict = message.parse_caption_entities()

		message_sentences_list = (
			self.__message_senteces_extractor.extract(
				message_text=message_text,
				message_entities_dict=message_entities_dict,
			)
		)

		del message
		del message_text
		del message_entities_dict

		if len(message_sentences_list) == 0:
			self.__logger.info('translate end [%s], nothing to translate', update_id)
			return None

		if self.__use_gcloud_f:

			translate_senteces_list = (
				await self.__translate_gcloud(
					username=username,
					language_code=language_code,
					message_sentences_list=message_sentences_list,
				)
			)

			translation = (
				self.__format_translation_reply(
					message_sentences_list=message_sentences_list,
					translate_senteces_list=translate_senteces_list,
				)
			)

		else:
			translation = (
				self.__format_translation_reply(
					message_sentences_list=message_sentences_list,
					translate_senteces_list=message_sentences_list,
				)
			)

		return translation


	async def __translate_gcloud(
			self,
			username: str,
			language_code: typing.Optional[str],
			message_sentences_list: list[str],
		) -> list[str]:

		translate_response = (
			await
			self.__gtranslate_client.translate_text(
				request=google.cloud.translate.TranslateTextRequest(
					parent=self.__config.gcloud_project_url,
					mime_type='text/plain',
					source_language_code='ro',
					target_language_code=(language_code or 'en'),
					contents=message_sentences_list,
					labels={
						'application': 'vladpy_telegram_ro_bot',
						'username': username[:GCLoudClientDefaults.label_max_length],
					},
				),
				timeout=GCLoudClientDefaults.request_timeout.total_seconds(),
				retry=google.api_core.retry_async.AsyncRetry(
					initial=GCLoudClientDefaults.request_retry_deltay_initial.total_seconds(),
					multiplier=GCLoudClientDefaults.request_retry_delay_multiplier,
					timeout=GCLoudClientDefaults.request_retry_timeout.total_seconds(),
				),
			)
		)

		translate_senteces_list = [
			translation_part.translated_text for translation_part in translate_response.translations
		]

		return translate_senteces_list


	def __detect_target_language(
			self,
			message_text: str,
			language_code: str,
			probability_threshold: float = .5,
		) -> bool:

		return (
			any((
				(
					(message_language.lang == language_code)
					and (message_language.prob >= probability_threshold)
				)
				for message_language in langdetect.detect_langs(message_text) # type: ignore
			))
		)


	def __format_translation_reply(
			self,
			message_sentences_list: list[str],
			translate_senteces_list: list[str],
		) -> str:

		assert len(message_sentences_list) == len(translate_senteces_list)

		translation = (
			(
				'>{message_sentence}\n{translation_sentence}\n'
				.format(
					message_sentence=telegram.helpers.escape_markdown(message_sentence, version=2,),
					translation_sentence=telegram.helpers.escape_markdown(translation_sentence, version=2,),
				)
			)
			for (message_sentence, translation_sentence) in zip(message_sentences_list, translate_senteces_list)
		)

		translation = '\n'.join(translation)

		return translation
