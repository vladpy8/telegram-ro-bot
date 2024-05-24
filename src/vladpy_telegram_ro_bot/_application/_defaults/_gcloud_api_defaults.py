from datetime import timedelta


class GCLoudApiDefaults:


	translate_text_contents_max_length = 1024
	translate_text_contents_cut_placeholder = '...'


	label_max_length = 63


	request_timeout = timedelta(seconds=60,)
