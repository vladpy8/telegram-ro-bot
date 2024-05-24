import re

import telegram
import telegram.helpers


class MessageSentencesExtractor:


	def __init__(self,) -> None:

		# TODO fix: quote handling
		# TODO fix: \xa0 symbol

		self.__regex_obj = (
			re.compile(
				pattern=('''
					[\n\t ]*([^[\n\t\\.?!;"]+[\\.?!;]*)
				'''),
				flags=re.MULTILINE,
			)
		)


	def extract(
			self,
			message_text: str,
			message_entities_dict: dict[telegram.MessageEntity, str],
		) -> list[str]:

		message_sentences_list: list[str] = []

		message_begin_index = 0
		message_end_index = 0

		for (message_entity, _) in message_entities_dict.items():

			if message_end_index < message_entity.offset:
				message_end_index = message_entity.offset

			if message_entity.type in {
					telegram.constants.MessageEntityType.BOLD,
					telegram.constants.MessageEntityType.CODE,
					telegram.constants.MessageEntityType.ITALIC,
					telegram.constants.MessageEntityType.SPOILER,
					telegram.constants.MessageEntityType.STRIKETHROUGH,
					telegram.constants.MessageEntityType.TEXT_LINK,
					telegram.constants.MessageEntityType.TEXT_MENTION,
					telegram.constants.MessageEntityType.UNDERLINE,
				}:

				message_end_index = message_entity.offset + message_entity.length

				continue

			if message_entity.type in {
					telegram.constants.MessageEntityType.BLOCKQUOTE,
					telegram.constants.MessageEntityType.PRE,
				}:

				message_sentences_list.extend((
					self.__extract_sentences_from_text_part(
						text=message_text,
						text_begin_index=message_begin_index,
						text_end_index=message_end_index,
					)
				))

				message_begin_index = message_entity.offset
				message_end_index = message_entity.offset + message_entity.length

			message_sentences_list.extend((
				self.__extract_sentences_from_text_part(
					text=message_text,
					text_begin_index=message_begin_index,
					text_end_index=message_end_index,
				)
			))

			message_end_index = message_entity.offset + message_entity.length
			message_begin_index = message_end_index

		message_end_index = len(message_text)

		if message_end_index != message_begin_index:

			message_sentences_list.extend((
				self.__extract_sentences_from_text_part(
					text=message_text,
					text_begin_index=message_begin_index,
					text_end_index=message_end_index,
				)
			))

		return message_sentences_list


	def __extract_sentences_from_text_part(
			self,
			text: str,
			text_begin_index: int,
			text_end_index: int,
		) -> list[str]:

		sentences = (
			match.group(1).rstrip('\n\t ') for match in (
				self.__regex_obj.finditer(
					string=text,
					pos=text_begin_index,
					endpos=text_end_index,
				)
			)
		)

		sentences = [sentence for sentence in sentences if len(sentence) > 0]

		return sentences
