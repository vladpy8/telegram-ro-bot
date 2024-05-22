import typing
import logging
import re

import telegram
import langdetect # type: ignore
#import google.cloud.translate


class Translator:


	def __init__(self,) -> None:

		self.__logger = logging.getLogger('vladpy_telegram_ro_bot.Translator')

		self.__logger.info('init')

		self.__regex_obj = (
			re.compile(
				pattern='[\n\t ]*([^[\n\t\\.?!;"]+[\\.?!;]*)',
				flags=re.MULTILINE,
			)
		)

		langdetect.DetectorFactory.seed = 0

		#self.__gtranslate_client = google.cloud.translate.TranslationServiceClient()


	def translate(
			self,
			update_id: int,
			message: telegram.Message,
		) -> typing.Optional[str]:

		assert message.text is not None

		self.__logger.info('translate begin [%s]', update_id)

		message_text = message.text

		message_target_language_detect_f = (
			self.__detect_target_language(
				message_text=message_text,
				language_code='ro',
			)
		)

		if not message_target_language_detect_f:
			self.__logger.info('translate end [%s], no target language', update_id)
			return None

		message_entities_dict: dict[telegram.MessageEntity, str] = message.parse_entities()

		translation_sentences_list = (
			self.__parse_translation_sentences(
				message_text=message_text,
				message_entities_dict=message_entities_dict,
			)
		)

		del message_text
		del message_entities_dict

		if len(translation_sentences_list) == 0:
			self.__logger.info('translate end [%s], nothing to translate', update_id)
			return None

		# response = (
		# 	self.__gtranslate_client.translate_text(
		# 		request={
		# 			'parent': 'projects/vladpy-ro-bot/locations/global',
		# 			'contents': ['Please translate me'],
		# 			'mime_type': 'text/plain',
		# 			'source_language_code': 'ro',
		# 			'target_language_code': 'ru',
		# 		}
		# 	)
		# )

		return '\n\n\t\n'.join(translation_sentences_list).replace(' ', '_')


	def __parse_translation_sentences(
			self,
			message_text: str,
			message_entities_dict: dict[telegram.MessageEntity, str],
		) -> list[str]:

		translation_sentences_list: list[str] = []

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

				translation_sentences_list.extend((
					self.__parse_sentences_from_text_part(
						text=message_text,
						text_begin_index=message_begin_index,
						text_end_index=message_end_index,
					)
				))

				message_begin_index = message_entity.offset
				message_end_index = message_entity.offset + message_entity.length

			translation_sentences_list.extend((
				self.__parse_sentences_from_text_part(
					text=message_text,
					text_begin_index=message_begin_index,
					text_end_index=message_end_index,
				)
			))

			message_end_index = message_entity.offset + message_entity.length
			message_begin_index = message_end_index

		message_end_index = len(message_text)

		if message_end_index != message_begin_index:

			translation_sentences_list.extend((
				self.__parse_sentences_from_text_part(
					text=message_text,
					text_begin_index=message_begin_index,
					text_end_index=message_end_index,
				)
			))

		return translation_sentences_list


	def __parse_sentences_from_text_part(
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


	def __detect_target_language(
			self,
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
