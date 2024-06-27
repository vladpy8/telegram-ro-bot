import textwrap

from vladpy_telegram_ro_bot._application._translator._translator_utils import detect_target_language


# TODO fix: tests
# TODO fix: add tests


def process_text(text: str,) -> str:

	text = (
		textwrap.dedent(text)
		.replace('\n', ' ')
		.strip(' \t\n\r')
	)

	return text


def test_short() -> None:

	assert (
		detect_target_language(
			language_code='ro',
			message_text=(
				process_text('''
					Сafeaua este cea mai bună băutură
				''')
			)
		)
	)


def test_short_mixed() -> None:

	assert (
		detect_target_language(
			language_code='ro',
			message_text=(
				process_text('''
					Bine. Bot este bine
				''')
			)
		)
	)

	assert (
		detect_target_language(
			language_code='ro',
			message_text=(
				process_text('''
					Eu am pisici
				''')
			)
		)
	)
