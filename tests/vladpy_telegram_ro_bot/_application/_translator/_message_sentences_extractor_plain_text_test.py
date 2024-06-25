from vladpy_telegram_ro_bot._application._translator._message_sentences_extractor import MessageSentencesExtractor


def test_simplest() -> None:

	sentences = (
		MessageSentencesExtractor().extract(
			message_text=('''
				Предложение 1
				Предложение 2
			'''),
			message_entities_dict=dict(),
		)
	)

	assert sentences == [
		'Предложение 1',
		'Предложение 2',
	]
