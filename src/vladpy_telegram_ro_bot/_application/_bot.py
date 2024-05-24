import typing
import logging
import concurrent.futures

import telegram
import telegram.ext
import telegram.error
import google.oauth2.service_account # type: ignore

from vladpy_telegram_ro_bot._application._text_invariant._command import Command
from vladpy_telegram_ro_bot._application._text_invariant._reply import Reply
from vladpy_telegram_ro_bot._application._translator._translator import Translator
from vladpy_telegram_ro_bot._application._translator._translate_result import TranslateResultCode
from vladpy_telegram_ro_bot._application._config._bot_config import BotConfig


# TODO improve: fast response in case of latency


class Bot:


	def __init__(
			self,
			config: BotConfig,
			gcloud_credentials: google.oauth2.service_account.Credentials,
			background_executor: concurrent.futures.Executor,
		) -> None:

		self.__logger = logging.getLogger('vladpy_telegram_ro_bot.Bot')

		self.__logger.info('init')

		self.__config = config

		self.__translator = (
			Translator(
				config=self.__config,
				gcloud_credentials=gcloud_credentials,
				background_executor=background_executor,
			)
		)


	async def handle_command(
			self,
			command: typing.Optional[telegram.BotCommand],
			update: telegram.Update,
			context: telegram.ext.ContextTypes.DEFAULT_TYPE,
		) -> None:

		self.__logger.info('command handle begin [%s]', update.update_id)

		if update.effective_chat is None:
			self.__logger.warning('command handle end [%s], no chat', update.update_id)
			return

		if update.effective_user is None:
			self.__logger.warning('command handle end [%s], no user', update.update_id)
			return

		if update.effective_user.is_bot:
			self.__logger.warning('command handle end [%s], user is bot', update.update_id)
			return

		if (
				self.__config.usernames_whitelist is not None
				and update.effective_user.username not in self.__config.usernames_whitelist
			):

			self.__logger.warning('command handle end [%s], user is not in whitelist', update.update_id)
			return

		message = update.message or update.edited_message

		if message is None:
			self.__logger.warning('command handle end [%s], no message', update.update_id)
			return

		language_code = update.effective_user.language_code

		if command == Command.hello_en:

			self.__logger.info('command handle "hello" [%s]', update.update_id)

			await (
				self.__reply_message(
					context=context,
					chat_id=update.effective_chat.id,
					update_id=update.update_id,
					message_id=message.id,
					text=Reply.hello(language_code),
				)
			)

		elif command == Command.help_en:

			self.__logger.info('command handle "help" [%s]', update.update_id)

			await (
				self.__reply_message(
					context=context,
					chat_id=update.effective_chat.id,
					update_id=update.update_id,
					message_id=message.id,
					text=Reply.help(language_code),
				)
			)

		elif command == Command.about_en:

			self.__logger.info('command handle "about" [%s]', update.update_id)

			await (
				self.__reply_message(
					context=context,
					chat_id=update.effective_chat.id,
					update_id=update.update_id,
					message_id=message.id,
					text=Reply.about(language_code),
				)
			)

		else:

			self.__logger.warning('command handle "unknown" [%s] "%s"', command, update.update_id)

			await (
				self.__reply_message(
					context=context,
					chat_id=update.effective_chat.id,
					update_id=update.update_id,
					message_id=message.id,
					text=Reply.unknown(language_code),
				)
			)

		self.__logger.info('command handle end [%s]', update.update_id)


	async def handle_translation(
			self,
			update: telegram.Update,
			context: telegram.ext.ContextTypes.DEFAULT_TYPE,
		) -> None:

		self.__logger.info('translation handle begin [%s]', update.update_id)

		if update.effective_chat is None:
			self.__logger.warning('translation handle end [%s], no chat', update.update_id)
			return

		if (
				update.effective_user is None
				or update.effective_user.username is None
			):
			self.__logger.warning('translation handle end [%s], no user', update.update_id)
			return

		if update.effective_user.is_bot:
			self.__logger.warning('translation handle end [%s], user bot', update.update_id)
			return

		if (
				self.__config.usernames_whitelist is not None
				and update.effective_user.username not in self.__config.usernames_whitelist
			):

			self.__logger.warning('translation handle end [%s], user not in whitelist', update.update_id)
			return

		if (
				sum((
					(update.message is not None),
					(update.edited_message is not None),
				))
				> 1
			):

			self.__logger.warning('translation handle [%s], message ambiguity', update.update_id)

		message = update.message or update.edited_message

		if message is None:
			self.__logger.warning('translation handle end [%s], no message', update.update_id)
			return

		language_code = update.effective_user.language_code

		translation = (
			await self.__translator.translate(
				update_id=update.update_id,
				message=message,
				language_code=language_code,
				username=update.effective_user.username,
			)
		)

		if translation.code == TranslateResultCode.QuotaReach:

			await (
				self.__reply_message(
					context=context,
					chat_id=update.effective_chat.id,
					update_id=update.update_id,
					message_id=message.id,
					text=Reply.quota_reach(language_code),
				)
			)

			self.__logger.info('translation handle end [%s], quota reach', update.update_id)
			return

		if translation.code != TranslateResultCode.Success:
			self.__logger.info('translation handle end [%s], no translation', update.update_id)
			return

		assert translation.text is not None

		await (
			self.__reply_message(
				context=context,
				chat_id=update.effective_chat.id,
				update_id=update.update_id,
				message_id=message.id,
				text=translation.text,
			)
		)

		self.__logger.info('translation handle end [%s]', update.update_id)


	async def __reply_message(
			self,
			context: telegram.ext.ContextTypes.DEFAULT_TYPE,
			chat_id: int,
			update_id: int,
			message_id: int,
			text: str,
		) -> None:

		try:

			await (
				context.bot.send_message(
					chat_id=chat_id,
					reply_parameters=(
						telegram.ReplyParameters(
							message_id=message_id,
						)
					),
					text=text,
				)
			)

		except telegram.error.Forbidden:
			self.__logger.info('message send exception [%s], forbidden', update_id)

		except:
			self.__logger.exception('message send exception [%s]', update_id)
			raise
