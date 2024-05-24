import dataclasses

import pydantic
import pydantic.dataclasses


@dataclasses.dataclass
class TelegramConfig:

	token: str


@pydantic.dataclasses.dataclass(
	config=pydantic.ConfigDict(
		frozen=True,
		strict=True,
		extra='forbid',
	),
)
class TelegramConfigPydantic(TelegramConfig):

	pass
