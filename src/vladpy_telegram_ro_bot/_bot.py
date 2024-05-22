import typing
import logging

import telegram
import telegram.ext
import telegram.error
import telegram.constants

from vladpy_telegram_ro_bot.constants._command import Command
from vladpy_telegram_ro_bot.constants._answer import Answer
from vladpy_telegram_ro_bot._translator import Translator


class Bot:


	def __init__(
			self,
			whitelist_usernames: set[str],
		) -> None:

		self.__logger = logging.getLogger('vladpy_telegram_ro_bot.Bot')

		self.__logger.info('init')

		self.__whitelist_usernames = whitelist_usernames

		self.__translator = Translator()


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

		if update.effective_user.username not in self.__whitelist_usernames:
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
					text=Answer.hello(language_code),
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
					text=Answer.help(language_code),
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
					text=Answer.about(language_code),
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
					text=Answer.unknown(language_code),
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

		if update.effective_user is None:
			self.__logger.warning('translation handle end [%s], no user', update.update_id)
			return

		if update.effective_user.is_bot:
			self.__logger.warning('translation handle end [%s], user bot', update.update_id)
			return

		if update.effective_user.username not in self.__whitelist_usernames:
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

		# TODO design: fast response in case of latency

		translation = (
			self.__translator.translate(
				update_id=update.update_id,
				message=message,
			)
		)

		if translation is None:
			self.__logger.info('translation handle end [%s], no translation', update.update_id)
			return

		await (
			self.__reply_message(
				context=context,
				chat_id=update.effective_chat.id,
				update_id=update.update_id,
				message_id=message.id,
				text=translation,
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
					parse_mode=telegram.constants.ParseMode.MARKDOWN_V2,
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
