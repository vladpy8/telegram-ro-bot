from datetime import timedelta


class GCLoudApiDefaults:


	# TODO debug
	translate_text_contents_max_length = 1024
	translate_text_contents_cut_placeholder = '...'


	label_max_length = 63


	request_timeout = timedelta(seconds=60,)

	request_retry_deltay_initial = timedelta(seconds=10,)
	request_retry_delay_multiplier = 1
	request_retry_timeout = timedelta(seconds=120,)
