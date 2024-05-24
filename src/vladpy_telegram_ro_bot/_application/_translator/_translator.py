import typing
import logging
import asyncio
import concurrent.futures
import functools
import copy

import telegram
import telegram.helpers
import langdetect # type: ignore
import google.cloud.translate
import google.api_core
import google.api_core.retry_async
import google.oauth2.service_account  # type: ignore

from vladpy_telegram_ro_bot._application._translator._translate_result import TranslateResult, TranslateResultCode
from vladpy_telegram_ro_bot._application._translator._message_sentences_extractor import MessageSentencesExtractor
from vladpy_telegram_ro_bot._application._config._bot_config import BotConfig
from vladpy_telegram_ro_bot._application._defaults._gcloud_client_defaults import GCLoudClientDefaults


langdetect.DetectorFactory.seed = 0


# TODO fix: add Google Translate attribution


class Translator:


	def __init__(
			self,
			config: BotConfig,
			gcloud_credentials: google.oauth2.service_account.Credentials,
			background_executor: concurrent.futures.Executor,
		) -> None:

		self.__logger = logging.getLogger('vladpy_telegram_ro_bot.Translator')

		self.__logger.info('init')

		self.__config = config
		self.__use_langdetect_f = False
		self.__use_gcloud_f = False

		self.__background_executor = background_executor

		self.__message_sentences_extractor = MessageSentencesExtractor()

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
		) -> TranslateResult:

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
			return TranslateResult(code=TranslateResultCode.NoTranslateText)

		message_target_language_detect_f = False

		if self.__use_langdetect_f:

			message_target_language_detect_f = (
				await asyncio.wrap_future(
					asyncio.get_event_loop().run_in_executor(
						self.__background_executor,
						functools.partial(
							Translator.__detect_target_language,
							message_text=message_text,
							language_code='ro',
						),
					)
				)
			)

			self.__logger.info('translate [%s], language detect', update_id)

		if (
				self.__use_langdetect_f
				and not message_target_language_detect_f
			):

			self.__logger.info('translate end [%s], no target language', update_id)
			return TranslateResult(code=TranslateResultCode.NoTargetLanguage)

		message_sentences_list = (
			await asyncio.wrap_future(
				asyncio.get_event_loop().run_in_executor(
					self.__background_executor,
					functools.partial(
						Translator.__extract_sentences_from_message,
						message_text=message_text,
						message=message,
						message_sentences_extractor=copy.deepcopy(self.__message_sentences_extractor),
					),
				)
			)
		)

		del message_text
		del message

		self.__logger.info('translate [%s], sentences extract', update_id)

		if len(message_sentences_list) == 0:
			self.__logger.info('translate end [%s], nothing to translate', update_id)
			return TranslateResult(code=TranslateResultCode.NoTranslateText)

		if self.__use_gcloud_f:

			self.__logger.info('translate [%s], gcloud request', update_id)

			translate_sentences_list = (
				await self.__translate_gcloud(
					username=username,
					language_code=language_code,
					message_sentences_list=message_sentences_list,
				)
			)

			self.__logger.info('translate [%s], gcloud response', update_id)

			translation = (
				await asyncio.wrap_future(
					asyncio.get_event_loop().run_in_executor(
						self.__background_executor,
						functools.partial(
							Translator.__format_translation_reply,
							message_sentences_list=message_sentences_list,
							translate_sentences_list=translate_sentences_list,
						),
					)
				)
			)

		else:

			self.__logger.info('translate [%s], dummy translation', update_id)

			translation = (
				await asyncio.wrap_future(
					asyncio.get_event_loop().run_in_executor(
						self.__background_executor,
						functools.partial(
							Translator.__format_translation_reply,
							message_sentences_list=message_sentences_list,
							translate_sentences_list=message_sentences_list,
						),
					)
				)
			)

		self.__logger.info('translate end [%s], success', update_id)

		return TranslateResult(code=TranslateResultCode.Success, translation=translation,)


	@staticmethod
	def __detect_target_language(
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


	@staticmethod
	def __extract_sentences_from_message(
			message_text: str,
			message: telegram.Message,
			message_sentences_extractor: MessageSentencesExtractor,
		) -> list[str]:

		message_entities_dict: dict[telegram.MessageEntity, str] = dict()

		if message.text is not None and len(message.text) > 0:
			message_entities_dict = message.parse_entities()

		elif message.caption is not None and len(message.caption) > 0:
			message_entities_dict = message.parse_caption_entities()

		message_sentences_list = (
			message_sentences_extractor.extract(
				message_text=message_text,
				message_entities_dict=message_entities_dict,
			)
		)

		return message_sentences_list


	@staticmethod
	def __format_translation_reply(
			message_sentences_list: list[str],
			translate_sentences_list: list[str],
		) -> str:

		assert len(message_sentences_list) == len(translate_sentences_list)

		escape_markdown_lambda = functools.partial(telegram.helpers.escape_markdown, version=2,)

		translation = (
			'\n'.join((
				f'>{message_sentence}\n{translation_sentence}\n'
				for (message_sentence, translation_sentence) in (
					zip(
						map(escape_markdown_lambda, message_sentences_list),
						map(escape_markdown_lambda, translate_sentences_list),
					)
				)
			))
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

		translate_sentences_list = [
			translation_part.translated_text for translation_part in translate_response.translations
		]

		return translate_sentences_list
