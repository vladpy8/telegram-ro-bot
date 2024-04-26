import json
import logging

import telegram
import telegram.ext

from _initiate_logs import initiate_logs

from _bot import Bot


class Application:


	def __init__(self,) -> None:

		self.__logger = logging.getLogger('telegram_ro_bot.Application')

		self.__application = None

		self._bot = Bot()


	def run(self,) -> None:

		initiate_logs()

		self.__create_appplication()
		assert self.__application is not None

		self.__application.run_polling()


	def __create_appplication(self,) -> None:

		self.__logger.info('create application begin')

		with (
				open(
					'config/.stash/telegram.json',
					mode='rt',
					encoding='utf8',
				)
			) as file_obj:

			telegram_token = json.load(file_obj)['token']

		self.__logger.info('toke read')

		self.__application = (
			telegram.ext.ApplicationBuilder()
			.token(telegram_token)
			.build()
		)

		self.__application.add_handler(
			telegram.ext.CommandHandler(
				callback=self._bot.handle_start,
				command='start',
			)
		)

		self.__application.add_handler(
			telegram.ext.MessageHandler(
				callback=self._bot.handle_message,
				filters=(telegram.ext.filters.TEXT & (~telegram.ext.filters.COMMAND)),
			)
		)

		self.__application.add_handler(
			telegram.ext.MessageHandler(
				callback=self._bot.handle_unknown_command,
				filters=telegram.ext.filters.COMMAND,
			)
		)

		self.__logger.info('create application end')
