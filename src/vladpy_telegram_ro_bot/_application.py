import json
import logging
import typing
import functools

import telegram
import telegram.ext

from vladpy_telegram_ro_bot._types import ApplicationType
from vladpy_telegram_ro_bot._initiate_logs import initiate_logs
from vladpy_telegram_ro_bot._application_defaults import ApplicationDefaults
from vladpy_telegram_ro_bot._bot import Bot
from vladpy_telegram_ro_bot.constants._command import Command
from vladpy_telegram_ro_bot.constants._answer import Answer


class Application:


	def __init__(self,) -> None:

		self.__logger = logging.getLogger('vladpy_telegram_ro_bot.Application')

		self.__logger.info('init')

		self.__application: typing.Optional[ApplicationType] = None

		self.__whitelist_usernames: typing.Optional[set[str]] = None
		self.__bot: typing.Optional[Bot] = None


	def run(self,) -> None:

		initiate_logs()

		self.__create_appplication()
		assert self.__application is not None

		self.__logger.info('run begin')

		# TODO run webhook option, though duplicate messages might arrive

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

		with (
				open(
					'config/.stash/whitelist.json',
					mode='rt',
					encoding='utf8',
				)
			) as file_obj:

			self.__whitelist_usernames = set(json.load(file_obj)['users'])

		self.__logger.info('whitelist read')

		self.__bot = (
			Bot(
				whitelist_usernames=self.__whitelist_usernames,
			)
		)

		# TODO implement persistence

		self.__application = (
			telegram.ext.ApplicationBuilder()
			.post_init(self.__initialize_application)
			.token(telegram_token)
			.concurrent_updates(True)
			.rate_limiter(telegram.ext.AIORateLimiter())
			.connect_timeout(ApplicationDefaults.connect_timeout.total_seconds())
			.pool_timeout(ApplicationDefaults.pool_timeout.total_seconds())
			.read_timeout(ApplicationDefaults.read_timeout.total_seconds())
			.write_timeout(ApplicationDefaults.write_timeout.total_seconds())
			.get_updates_connect_timeout(ApplicationDefaults.get_updates_connect_timeout.total_seconds())
			.get_updates_pool_timeout(ApplicationDefaults.get_updates_pool_timeout.total_seconds())
			.get_updates_read_timeout(ApplicationDefaults.get_updates_read_timeout.total_seconds())
			.get_updates_write_timeout(ApplicationDefaults.get_updates_write_timeout.total_seconds())
			.build()
		)

		self.__logger.info('create application end')


	async def __initialize_application(
			self,
			application: ApplicationType,
		) -> None:

		self.__logger.info('initialize begin')

		assert self.__whitelist_usernames is not None
		assert self.__bot is not None
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

		application.add_error_handler(self.__handle_error)

		chat_whitelist_usernames_filter = telegram.ext.filters.Chat()
		chat_whitelist_usernames_filter.add_usernames(self.__whitelist_usernames)

		for command in Command.command_sequence(None):

			application.add_handler(
				telegram.ext.CommandHandler(
					command=command.command,
					filters=(
						telegram.ext.filters.COMMAND
						& telegram.ext.filters.USER
						& telegram.ext.filters.CHAT
						& (~telegram.ext.filters.VIA_BOT)
						& chat_whitelist_usernames_filter
					),
					callback=functools.partial(self.__bot.handle_command, command,),
					block=False,
					has_args=False,
				)
			)

		application.add_handler(
			telegram.ext.MessageHandler(
				filters=(
					telegram.ext.filters.TEXT
					& (~telegram.ext.filters.COMMAND)
					& telegram.ext.filters.USER
					& telegram.ext.filters.CHAT
					& (~telegram.ext.filters.VIA_BOT)
					& chat_whitelist_usernames_filter
				),
				callback=self.__bot.handle_translation,
				block=False,
			)
		)

		self.__logger.info('initialize end')


	async def __handle_error(
			self,
			_: typing.Any,
			context: telegram.ext.ContextTypes.DEFAULT_TYPE,
		) -> None:

		# TODO send message to admin
		# TODO consider stopping app

		self.__logger.exception('application error: %s', context.error, exc_info=True,)
