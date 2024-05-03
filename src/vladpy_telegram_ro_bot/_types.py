import typing

import telegram
import telegram.ext


BotType = telegram.ext.ExtBot[int]


UserDataType = dict[typing.Any, typing.Any]


ChatDataType = dict[typing.Any, typing.Any]


BotDataType = dict[typing.Any, typing.Any]


CallbackContextType = (
	telegram.ext.CallbackContext[
		telegram.ext.ExtBot[None],
		UserDataType,
		ChatDataType,
		BotDataType,
	]
)


ApplicationType = (
	telegram.ext.Application[
		BotType,
		CallbackContextType,
		UserDataType,
		ChatDataType,
		BotDataType,
		telegram.ext.JobQueue[CallbackContextType],
	]
)
