from datetime import timedelta


class ApplicationDefaults:


	connect_timeout = timedelta(seconds=30,)
	pool_timeout = timedelta(seconds=10,)
	read_timeout = timedelta(seconds=30,)
	write_timeout = timedelta(seconds=30,)


	get_updates_connect_timeout = timedelta(seconds=30,)
	get_updates_pool_timeout = timedelta(seconds=10,)
	get_updates_read_timeout = timedelta(seconds=30,)
	get_updates_write_timeout = timedelta(seconds=30,)
