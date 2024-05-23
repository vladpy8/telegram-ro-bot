import typing
from textwrap import dedent

import telegram


class Command:


	@staticmethod
	def reduce_language_code(language_code: typing.Optional[str],) -> str:

		language_code_loc = language_code

		if (
				language_code_loc is None
				or language_code_loc not in (
					'en',
					'ru',
				)
			):

			language_code_loc = 'en'

		return language_code_loc


	@staticmethod
	def process_text(text: str,) -> str:

		return (
			dedent(text)
			.replace('\n', ' ')
			.strip(' \t\n\r')
		)


	hello_en: telegram.BotCommand = (
		telegram.BotCommand(
			command='hello',
			description=process_text('''
				Greet Bot and launch conversation
			''')
		)
	)


	hello_ru: telegram.BotCommand = (
		telegram.BotCommand(
			command='hello',
			description=process_text('''
				Скажи Боту привет и запусти общение
			''')
		)
	)


	# TODO
	help_en: telegram.BotCommand = (
		telegram.BotCommand(
			command='help',
			description=process_text('''
				HELP STUB
			''')
		)
	)


	# TODO
	help_ru: telegram.BotCommand = (
		telegram.BotCommand(
			command='help',
			description=process_text('''
				HELP STUB
			''')
		)
	)


	# TODO
	about_en: telegram.BotCommand = (
		telegram.BotCommand(
			command='about',
			description=process_text('''
				ABOUT STUB
			''')
		)
	)


	# TODO
	about_ru: telegram.BotCommand = (
		telegram.BotCommand(
			command='about',
			description=process_text('''
				ABOUT STUB
			''')
		)
	)


	@staticmethod
	def command_sequence(language_code: typing.Optional[str],) -> tuple[telegram.BotCommand, ...]:

		return (
			({
				'en': (
					Command.hello_en,
					Command.help_en,
					Command.about_en,
				),
				'ru': (
					Command.hello_ru,
					Command.help_ru,
					Command.about_ru,
				)
			})
			[Command.reduce_language_code(language_code)]
		)
