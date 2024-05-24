import logging
import typing
import pathlib
import sys


# TODO fix: multithreaded logging
# TODO fix: create file when absent
# TODO fix: multiple files with archiving
# TODO improve: use gcloud logging


def initiate_logs(
		stream_f: bool = False,
		file_f: bool = True,
		file_path: typing.Optional[pathlib.Path] = None,
	) -> None:

	logger = logging.getLogger()

	logger.setLevel(logging.DEBUG)

	file_path_loc = file_path or 'logs/vladpy_telegram_ro_bot.log'

	if stream_f:
		logger.addHandler(logging.StreamHandler(stream=sys.stdout,))

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

		logger.addHandler(file_handler)

	logging.getLogger('httpx').setLevel(logging.WARNING)
	logging.getLogger('httpcore').setLevel(logging.WARNING)
	logging.getLogger('apscheduler').setLevel(logging.WARNING)

	logger.info('logging init')
