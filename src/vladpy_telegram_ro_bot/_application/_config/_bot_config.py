import typing
import dataclasses

import pydantic
import pydantic.dataclasses


@dataclasses.dataclass
class BotConfig:

	gcloud_project_url: str
	gcloud_application_label: str

	usernames_admin: tuple[str, ...]
	usernames_whitelist: typing.Optional[tuple[str, ...]] = None

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
