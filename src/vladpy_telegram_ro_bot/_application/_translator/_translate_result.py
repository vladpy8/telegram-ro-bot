import typing
import dataclasses
import enum


class TranslateResultCode(enum.IntEnum):

	Success = 0

	NoTranslateText = 1
	NoTargetLanguage = 2

	QuotaReach = 3


@dataclasses.dataclass
class TranslateResult:

	code: TranslateResultCode
	text: typing.Optional[str] = None
