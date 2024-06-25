from vladpy_telegram_ro_bot._application._translator._message_sentences_extractor import MessageSentencesExtractor


# TODO fix: tests
# TODO fix: add tests


def test_simplest() -> None:

	sentences = (
		MessageSentencesExtractor().extract(
			message_text=('''
				Sentence 1
				Sentence 2.    Sentence 3!
						Sentence 4   ?
				Sentence 5, complex one
			'''),
			message_entities_dict=dict(),
		)
	)

	assert (
		sentences == [
			'Sentence 1',
			'Sentence 2.',
			'Sentence 3!',
			'Sentence 4   ?',
			'Sentence 5, complex one',
		]
	)


def test_date() -> None:

	sentences = (
		MessageSentencesExtractor().extract(
			message_text=('''
				Event happened on 2024.05.30, and then another event happened
			'''),
			message_entities_dict=dict(),
		)
	)

	assert (
		sentences == [
			'Event happened on 2024.05.30, and then another event happened',
		]
	)


def test_special_symbols() -> None:

	sentences = (
		MessageSentencesExtractor().extract(
			message_text=('''
				Sentence with special symbols littered across it
			'''),
			message_entities_dict=dict(),
		)
	)

	assert (
		sentences == [
			'Sentence with special symbols littered across it',
		]
	)
