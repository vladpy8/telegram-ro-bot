import dataclasses

import pydantic
import pydantic.dataclasses


@dataclasses.dataclass
class BotConfig:

	gcloud_project_url: str

	users_admin: tuple[str, ...]
	users_whitelist: tuple[str, ...]

	use_gcloud_f: bool = False
	use_langdetect_f: bool = False


@pydantic.dataclasses.dataclass(
	config=pydantic.ConfigDict(
		frozen=True,
		strict=True,
		extra='forbid',
	),
)
class BotConfigPydantic(BotConfig):

	pass
