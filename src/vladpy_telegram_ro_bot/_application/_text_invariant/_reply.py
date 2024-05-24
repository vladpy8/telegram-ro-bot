import typing
from textwrap import dedent

import telegram.helpers


# TODO fix: add Google Translate attribution
# TODO fix: stubs
# TODO fix: points need covering:
#    - usage example
#    - only selected messages got reply


class Reply:


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
				'en': Reply.hello_en,
				'ru': Reply.hello_ru,
			})
			[Reply.reduce_language_code(language_code)]
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
				'en': Reply.unknown_en,
				'ru': Reply.unknown_ru,
			})
			[Reply.reduce_language_code(language_code)]
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
				'en': Reply.help_en,
				'ru': Reply.help_ru,
			})
			[Reply.reduce_language_code(language_code)]
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
				'en': Reply.about_en,
				'ru': Reply.about_ru,
			})
			[Reply.reduce_language_code(language_code)]
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
				'en': Reply.description_en,
				'ru': Reply.description_ru,
			})
			[Reply.reduce_language_code(language_code)]
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
				'en': Reply.short_description_en,
				'ru': Reply.short_description_ru,
			})
			[Reply.reduce_language_code(language_code)]
		)


	quota_reach_en: str = (
		process_text('''
			QUOTA LIMIT STUB
		''')
	)

	quota_reach_ru: str = (
		process_text('''
			QUOTA LIMIT STUB
		''')
	)

	@staticmethod
	def quota_reach(language_code: typing.Optional[str],) -> str:

		return (
			({
				'en': Reply.quota_reach_en,
				'ru': Reply.quota_reach_ru,
			})
			[Reply.reduce_language_code(language_code)]
		)
