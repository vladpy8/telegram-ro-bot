import typing
import dataclasses
import enum


class TranslateResultCode(enum.IntEnum):

	Success = 0
	NoTranslateText = 1
	NoTargetLanguage = 2


@dataclasses.dataclass
class TranslateResult:

	code: TranslateResultCode
	translation: typing.Optional[str] = None
