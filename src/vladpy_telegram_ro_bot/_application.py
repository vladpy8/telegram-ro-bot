import json
import logging
import typing

import telegram
import telegram.ext

from vladpy_telegram_ro_bot._initiate_logs import initiate_logs
from vladpy_telegram_ro_bot._bot import Bot


class Application:


	def __init__(self,) -> None:

		self.__logger = logging.getLogger('vladpy_telegram_ro_bot.Application')

		self.__logger.info('init')

		self.__application: typing.Optional[telegram.ext.Application] = None

		self.__bot = Bot()


	def run(self,) -> None:

		initiate_logs()

		self.__create_appplication()
		assert self.__application is not None

		self.__logger.info('application run begin')

		# TODO run webhook

		self.__application.run_polling()

		self.__logger.info('application run end')


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
				callback=self.__bot.handle_command,
				command=(
					'hello',
					'help',
					'about',
				),
			)
		)

		self.__application.add_handler(
			telegram.ext.MessageHandler(
				callback=self.__bot.handle_translation,
				filters=(telegram.ext.filters.TEXT & (~telegram.ext.filters.COMMAND)),
			)
		)

		self.__application.add_handler(
			telegram.ext.MessageHandler(
				callback=self.__bot.handle_command,
				filters=telegram.ext.filters.COMMAND,
			)
		)

		self.__logger.info('create application end')
