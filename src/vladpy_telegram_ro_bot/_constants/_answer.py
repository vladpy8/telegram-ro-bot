import typing
from textwrap import dedent


# TODO fix: add Google Translate attribution
# TODO fix: stubs


class Answer:


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


	hello_en: str = (
		process_text('''
			Hello. This is Romanian translator Bot. Please, send me romanian text and I will translate it for you,
			sentence by sentence.
		''')
	)

	hello_ru: str = (
		process_text('''
			Привет. Это бот переводчик с румынского. Пожалуйста, пришли мне текст на румынском и я его перевду для тебя,
			предложение за предложением.
		''')
	)

	@staticmethod
	def hello(language_code: typing.Optional[str],) -> str:

		return (
			({
				'en': Answer.hello_en,
				'ru': Answer.hello_ru,
			})
			[Answer.reduce_language_code(language_code)]
		)


	unknown_en: str = (
		process_text('''
			Don't understand you
		''')
	)

	unknown_ru: str = (
		process_text('''
			Не понимаю тебя
		''')
	)

	@staticmethod
	def unknown(language_code: typing.Optional[str],) -> str:

		return (
			({
				'en': Answer.unknown_en,
				'ru': Answer.unknown_ru,
			})
			[Answer.reduce_language_code(language_code)]
		)


	help_en: str = (
		process_text('''
			HELP STUB
		''')
	)

	help_ru: str = (
		process_text('''
			HELP STUB
		''')
	)

	@staticmethod
	def help(language_code: typing.Optional[str],) -> str:

		return (
			({
				'en': Answer.help_en,
				'ru': Answer.help_ru,
			})
			[Answer.reduce_language_code(language_code)]
		)


	about_en: str = (
		process_text('''
			ABOUT STUB
		''')
	)

	about_ru: str = (
		process_text('''
			ABOUT STUB
		''')
	)

	@staticmethod
	def about(language_code: typing.Optional[str],) -> str:

		return (
			({
				'en': Answer.about_en,
				'ru': Answer.about_ru,
			})
			[Answer.reduce_language_code(language_code)]
		)


	description_en: str = (
		process_text('''
			DESCRIPTION STUB
		''')
	)

	description_ru: str = (
		process_text('''
			DESCRIPTION STUB
		''')
	)

	@staticmethod
	def description(language_code: typing.Optional[str],) -> str:

		return (
			({
				'en': Answer.description_en,
				'ru': Answer.description_ru,
			})
			[Answer.reduce_language_code(language_code)]
		)


	short_description_en: str = (
		process_text('''
			SHORT DESCRIPTION STUB
		''')
	)

	short_description_ru: str = (
		process_text('''
			SHORT DESCRIPTION STUB
		''')
	)

	@staticmethod
	def short_description(language_code: typing.Optional[str],) -> str:

		return (
			({
				'en': Answer.short_description_en,
				'ru': Answer.short_description_ru,
			})
			[Answer.reduce_language_code(language_code)]
		)
