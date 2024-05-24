import functools

import telegram
import langdetect # type: ignore

from vladpy_telegram_ro_bot._application._translator._message_sentences_extractor import MessageSentencesExtractor


langdetect.DetectorFactory.seed = 0


def detect_target_language(
		message_text: str,
		language_code: str,
		probability_threshold: float = .5,
	) -> bool:

	return (
		any((
			(
				(message_language.lang == language_code)
				and (message_language.prob >= probability_threshold)
			)
			for message_language in langdetect.detect_langs(message_text) # type: ignore
		))
	)


def extract_sentences_from_message(
		message_text: str,
		message: telegram.Message,
		message_sentences_extractor: MessageSentencesExtractor,
	) -> list[str]:

	message_entities_dict: dict[telegram.MessageEntity, str] = dict()

	if message.text is not None and len(message.text) > 0:
		message_entities_dict = message.parse_entities()

	elif message.caption is not None and len(message.caption) > 0:
		message_entities_dict = message.parse_caption_entities()

	message_sentences_list = (
		message_sentences_extractor.extract(
			message_text=message_text,
			message_entities_dict=message_entities_dict,
		)
	)

	return message_sentences_list


def format_translation_reply(
		message_sentences_list: list[str],
		translate_sentences_list: list[str],
		translation_cut_f: bool,
	) -> str:

	assert len(message_sentences_list) == len(translate_sentences_list)

	escape_markdown_lambda = functools.partial(telegram.helpers.escape_markdown, version=2,)

	translation = (
		'\n'.join((
			f'>{message_sentence}\n{translation_sentence}\n'
			for (message_sentence, translation_sentence) in (
				zip(
					map(escape_markdown_lambda, message_sentences_list),
					map(escape_markdown_lambda, translate_sentences_list),
				)
			)
		))
	)

	if translation_cut_f:
		translation = translation + escape_markdown_lambda('\n...')

	return translation
