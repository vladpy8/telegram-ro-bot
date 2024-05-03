import json
import logging
import typing

import telegram
import telegram.ext

from vladpy_telegram_ro_bot._types import ApplicationType
from vladpy_telegram_ro_bot._initiate_logs import initiate_logs
from vladpy_telegram_ro_bot._bot import Bot
from vladpy_telegram_ro_bot.constants._command import Command
from vladpy_telegram_ro_bot.constants._answer import Answer


class Application:


	def __init__(self,) -> None:

		self.__logger = logging.getLogger('vladpy_telegram_ro_bot.Application')

		self.__logger.info('init')

		self.__application: typing.Optional[ApplicationType] = None

		self.__bot = Bot()


	def run(self,) -> None:

		initiate_logs()

		self.__create_appplication()
		assert self.__application is not None

		self.__logger.info('run begin')

		# TODO run webhook option

		self.__application.run_polling()

		self.__logger.info('run end')


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

		self.__logger.info('token read')

		self.__application = (
			telegram.ext.ApplicationBuilder()
			.token(telegram_token)
			.concurrent_updates(True)
			.rate_limiter(telegram.ext.AIORateLimiter())
			.post_init(self.__initialize_application)
			.build()
		)

		self.__logger.info('create application end')


	async def __initialize_application(
			self,
			application: ApplicationType,
		) -> None:

		self.__logger.info('initialize begin')

		assert application.bot is not None

		await application.bot.set_my_commands(
			commands=tuple(Command.command_sequence(None)),
		)

		await application.bot.set_my_commands(
			commands=tuple(Command.command_sequence('ru')),
			language_code='ru',
		)

		self.__logger.info('bot commands set')

		await application.bot.set_my_description(
			description=Answer.description(None),
		)

		await application.bot.set_my_description(
			description=Answer.description('ru'),
			language_code='ru',
		)

		await application.bot.set_my_short_description(
			short_description=Answer.short_description(None),
		)

		await application.bot.set_my_short_description(
			short_description=Answer.short_description('ru'),
			language_code='ru',
		)

		self.__logger.info('bot description set')

		application.add_handler(
			telegram.ext.CommandHandler(
				callback=self.__bot.handle_command,
				block=False,
				command=tuple((
					command.command for command in (
						*Command.command_sequence(None),
						*Command.command_sequence('ru'),
					)
				)),
			)
		)

		application.add_handler(
			telegram.ext.MessageHandler(
				callback=self.__bot.handle_translation,
				block=False,
				filters=(telegram.ext.filters.TEXT & (~telegram.ext.filters.COMMAND)),
			)
		)

		application.add_handler(
			telegram.ext.MessageHandler(
				callback=self.__bot.handle_command,
				block=False,
				filters=telegram.ext.filters.COMMAND,
			)
		)

		self.__logger.info('initialize end')
