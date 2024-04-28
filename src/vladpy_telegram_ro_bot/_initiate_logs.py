import logging
import typing
import pathlib
import sys


def initiate_logs(
		stream_f: bool = False,
		file_f: bool = True,
		file_path: typing.Optional[pathlib.Path] = None,
	):

	logging.getLogger('vladpy_telegram_ro_bot').setLevel(logging.DEBUG)

	file_path_loc = file_path or 'logs/vladpy_telegram_ro_bot.log'

	if stream_f:
		logging.getLogger('vladpy_telegram_ro_bot').addHandler(logging.StreamHandler(stream=sys.stdout,))

	if file_f:

		file_handler = (
			logging.FileHandler(
				filename=file_path_loc,
				encoding='utf-8',
			)
		)

		file_handler.setFormatter(
			logging.Formatter(
				fmt=(
					'{asctime} P{process}|T{thread}'
					'\n\t{name} {levelname}'
					'\n\t{message}'
				),
				style='{',
				validate=True,
			)
		)

		logging.getLogger('vladpy_telegram_ro_bot').addHandler(file_handler)

	logging.getLogger('vladpy_telegram_ro_bot').info('logging init')
