import typing
from textwrap import dedent


class Message:


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


	hello_en: str = (
		dedent('''
			Hello. This is Romanian translator Bot. Please, send me romanian text and I will translate it to your
			language, sentence by sentence.
		''')
		.replace('\n', ' ')
		.strip(' \t\n\r')
	)


	hello_ru: str = (
		dedent('''
			Привет. Это бот переводчик с румынского. Пожалуйста, пришли мне текст на румынском и я его перевду для тебя,
			предложение за предложением.
		''')
		.replace('\n', ' ')
		.strip(' \t\n\r')
	)


	@staticmethod
	def hello(language_code: typing.Optional[str],) -> str:

		return (
			({
				'en': Message.hello_en,
				'ru': Message.hello_ru,
			})
			[Message.reduce_language_code(language_code)]
		)


	unknown_en: str = (
		dedent('''
			Don't understand you
		''')
		.replace('\n', ' ')
		.strip(' \t\n\r')
	)


	unknown_ru: str = (
		dedent('''
			Не понимаю тебя
		''')
		.replace('\n', ' ')
		.strip(' \t\n\r')
	)


	@staticmethod
	def unknown(language_code: typing.Optional[str],) -> str:

		return (
			({
				'en': Message.unknown_en,
				'ru': Message.unknown_ru,
			})
			[Message.reduce_language_code(language_code)]
		)


	help_en: str = (
		# TODO
		dedent('''
			HELP STUB
		''')
		.replace('\n', ' ')
		.strip(' \t\n\r')
	)


	help_ru: str = (
		# TODO
		dedent('''
			HELP STUB
		''')
		.replace('\n', ' ')
		.strip(' \t\n\r')
	)


	@staticmethod
	def help(language_code: typing.Optional[str],) -> str:

		return (
			({
				'en': Message.help_en,
				'ru': Message.help_ru,
			})
			[Message.reduce_language_code(language_code)]
		)


	about_en: str = (
		# TODO
		dedent('''
			ABOUT STUB
		''')
		.replace('\n', ' ')
		.strip(' \t\n\r')
	)


	about_ru: str = (
		# TODO
		dedent('''
			ABOUT STUB
		''')
		.replace('\n', ' ')
		.strip(' \t\n\r')
	)


	@staticmethod
	def about(language_code: typing.Optional[str],) -> str:

		return (
			({
				'en': Message.about_en,
				'ru': Message.about_ru,
			})
			[Message.reduce_language_code(language_code)]
		)
