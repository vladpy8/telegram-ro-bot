import typing
import logging
import asyncio
import concurrent.futures
import functools
import copy

import telegram
import telegram.helpers

import google.cloud.translate
import google.api_core
import google.api_core.retry_async
import google.api_core.exceptions
import google.oauth2.service_account  # type: ignore

from vladpy_telegram_ro_bot._application._translator._translate_result import TranslateResult, TranslateResultCode
from vladpy_telegram_ro_bot._application._translator._message_sentences_extractor import MessageSentencesExtractor
from vladpy_telegram_ro_bot._application._translator._translator_utils import (
	detect_target_language,
	extract_sentences_from_message,
	format_translation_reply,
)

from vladpy_telegram_ro_bot._application._config._bot_config import BotConfig
from vladpy_telegram_ro_bot._application._defaults._gcloud_api_defaults import GCLoudApiDefaults


# TODO fix: add Google Translate attribution
# TODO feature: send message to admin in case of quota reach


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

		if message_text is None or len(message_text) == 0:
			self.__logger.warning('translate end [%s], no text', update_id)
			return TranslateResult(code=TranslateResultCode.NoTranslateText)

		message_target_language_detect_f = False

		if self.__use_langdetect_f:

			message_target_language_detect_f = (
				await asyncio.wrap_future(
					asyncio.get_event_loop().run_in_executor(
						self.__background_executor,
						functools.partial(
							detect_target_language,
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
						extract_sentences_from_message,
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

			translation_cut_f = False

			if len(message_sentences_list) > GCLoudApiDefaults.translate_text_contents_max_length:

				self.__logger.info('translate [%s], translation cut', update_id)

				translation_cut_f = True
				message_sentences_list = (
					message_sentences_list[:GCLoudApiDefaults.translate_text_contents_max_length]
				)

			(
				translation_code,
				translate_sentences_list,
			) = (
				await self.__translate_gcloud(
					update_id=update_id,
					username=username,
					language_code=language_code,
					message_sentences_list=message_sentences_list,
				)
			)

			translation_reply = None

			if translate_sentences_list is not None:

				translation_reply = (
					await asyncio.wrap_future(
						asyncio.get_event_loop().run_in_executor(
							self.__background_executor,
							functools.partial(
								format_translation_reply,
								message_sentences_list=message_sentences_list,
								translate_sentences_list=translate_sentences_list,
								translation_cut_f=translation_cut_f,
							),
						)
					)
				)

		else:

			translation_code = TranslateResultCode.Success

			translation_reply = (
				await asyncio.wrap_future(
					asyncio.get_event_loop().run_in_executor(
						self.__background_executor,
						functools.partial(
							format_translation_reply,
							message_sentences_list=message_sentences_list,
							translate_sentences_list=message_sentences_list,
							translation_cut_f=False,
						),
					)
				)
			)

			self.__logger.info('translate [%s], dummy translation', update_id)

		self.__logger.info('translate end [%s], success', update_id)

		return TranslateResult(code=translation_code, text=translation_reply,)


	async def __translate_gcloud(
			self,
			update_id: int,
			username: str,
			language_code: typing.Optional[str],
			message_sentences_list: list[str],
		) -> tuple[TranslateResultCode, typing.Optional[list[str]]]:

		self.__logger.info('translate gcloud begin [%s]', update_id)

		language_code = language_code or 'en'
		if language_code == 'ro':
			language_code = 'en'

		try:

			translate_response = (
				await self.__gtranslate_client.translate_text(
					request=google.cloud.translate.TranslateTextRequest(
						parent=self.__config.gcloud_project_url,
						mime_type='text/plain',
						source_language_code='ro',
						target_language_code=language_code,
						contents=message_sentences_list,
						labels={
							'application': self.__config.gcloud_application_label,
							'username': username[:GCLoudApiDefaults.label_max_length].lower(),
						},
					),
					timeout=GCLoudApiDefaults.request_timeout.total_seconds(),
				)
			)

			translate_sentences_list = [
				translation_part.translated_text for translation_part in translate_response.translations
			]

		except google.api_core.exceptions.ResourceExhausted:

			self.__logger.warning('translate gcloud exception [%s], quota reach', update_id)

			self.__logger.info('translate gcloud end [%s]', update_id)

			return (TranslateResultCode.QuotaReach, None)

		except:

			self.__logger.exception('translate gcloud exception [%s]', update_id)
			raise

		self.__logger.info('translate gcloud end [%s]', update_id)

		return (TranslateResultCode.Success, translate_sentences_list)
