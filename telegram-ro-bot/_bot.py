import logging

import telegram
import telegram.ext


class Bot:


	def __init__(self,) -> None:

		self.__logger = logging.getLogger('telegram_ro_bot.Bot')


	async def handle_start(
			self,
			update: telegram.Update,
			context: telegram.ext.ContextTypes.DEFAULT_TYPE
		) -> None:

		self.__logger.info('start handle begin')

		assert update.effective_chat is not None

		await (
			context.bot.send_message(
				chat_id=update.effective_chat.id,
				text='''I'm a bot, please talk to me!''',
			)
		)

		self.__logger.info('start handle end')


	async def handle_message(
			self,
			update: telegram.Update,
			context: telegram.ext.ContextTypes.DEFAULT_TYPE
		) -> None:

		self.__logger.info('message handle begin')

		assert update.effective_chat is not None

		await (
			context.bot.send_message(
				chat_id=update.effective_chat.id,
				text='''Received your message. Please wait''',
			)
		)

		self.__logger.info('message handle end')


	async def handle_unknown_command(
			self,
			update: telegram.Update,
			context: telegram.ext.ContextTypes.DEFAULT_TYPE
		) -> None:

		self.__logger.info('unknown command handle begin')

		assert update.effective_chat is not None

		await (
			context.bot.send_message(
				chat_id=update.effective_chat.id,
				text='''Beyond me''',
			)
		)

		self.__logger.info('unknown command handle end')
