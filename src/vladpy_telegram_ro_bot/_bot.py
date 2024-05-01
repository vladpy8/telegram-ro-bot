import typing
import logging

import telegram
import telegram.ext

from vladpy_telegram_ro_bot._message import Message


class Bot:


	def __init__(self,) -> None:

		self.__logger = logging.getLogger('vladpy_telegram_ro_bot.Bot')

		self.__logger.info('init')


	async def handle_command(
			self,
			update: telegram.Update,
			context: telegram.ext.ContextTypes.DEFAULT_TYPE,
		) -> None:

		self.__logger.info('command handle begin: %s', update.update_id)

		if update.effective_chat is None:
			self.__logger.info('command handle, no chat: %s', update.update_id)
			return

		if (
				update.message is None
				or update.message.text is None
			):
			self.__logger.info('command handle, no message: %s', update.update_id)
			return

		language_code: typing.Optional[str] = None

		if update.effective_user is not None:
			language_code = update.effective_user.language_code

		command: str = update.message.text.split(' ')[0].strip(' \t\n\r')

		if command == '/hello':

			self.__logger.info('command handle, hello: %s', update.update_id)

			await (
				context.bot.send_message(
					chat_id=update.effective_chat.id,
					text=Message.hello(language_code),
				)
			)

		elif command == '/help':

			self.__logger.info('command handle, help: %s', update.update_id)

			await (
				context.bot.send_message(
					chat_id=update.effective_chat.id,
					text=Message.help(language_code),
				)
			)

		elif command == '/about':

			self.__logger.info('command handle, about: %s', update.update_id)

			await (
				context.bot.send_message(
					chat_id=update.effective_chat.id,
					text=Message.about(language_code),
				)
			)

		else:

			self.__logger.warning('command handle, unknown command "%s": %s', command, update.update_id)

			await (
				context.bot.send_message(
					chat_id=update.effective_chat.id,
					text=Message.unknown(language_code),
				)
			)

		self.__logger.info('command handle end: %s', update.update_id)


	async def handle_translation(
			self,
			update: telegram.Update,
			context: telegram.ext.ContextTypes.DEFAULT_TYPE
		) -> None:

		self.__logger.info('translation handle begin: %s', update.update_id)

		assert update.effective_chat is not None

		await (
			context.bot.send_message(
				chat_id=update.effective_chat.id,
				text='''Перевожу''',
			)
		)

		self.__logger.info('translation handle end: %s', update.update_id)
