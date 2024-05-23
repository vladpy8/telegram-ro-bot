import dataclasses

import pydantic
import pydantic.dataclasses


@dataclasses.dataclass
class BotConfig:

	gcloud_project_url: str

	usernames_admin: tuple[str, ...]
	usernames_whitelist: tuple[str, ...]

	use_langdetect_f: bool = False
	use_gcloud_f: bool = False


@pydantic.dataclasses.dataclass(
	config=pydantic.ConfigDict(
		frozen=True,
		strict=True,
		extra='forbid',
	),
)
class BotConfigPydantic(BotConfig):

	pass
