import typing
from textwrap import dedent

import telegram


# TODO fix: add Google Translate attribution
# TODO fix: stubs

# TODO feature: feedback command
# TODO architecture: admin commands


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

		text = (
			dedent(text)
			.replace('\n', ' ')
			.strip(' \t\n\r')
		)

		text = telegram.helpers.escape_markdown(text=text, version=2,)

		return text


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


	help_en: telegram.BotCommand = (
		telegram.BotCommand(
			command='help',
			description=process_text('''
				HELP STUB
			''')
		)
	)

	help_ru: telegram.BotCommand = (
		telegram.BotCommand(
			command='help',
			description=process_text('''
				HELP STUB
			''')
		)
	)


	about_en: telegram.BotCommand = (
		telegram.BotCommand(
			command='about',
			description=process_text('''
				ABOUT STUB
			''')
		)
	)

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
