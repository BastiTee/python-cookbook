import logging

LOGGING_FORMAT='[%(levelname)s]\t%(message)s'
"""Default logging format"""

def setup_logging(debug=False):
	if debug:
		logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT)
	else:
		logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)
	logging.info('Log level INFO enabled.')
	logging.debug('Log level DEBUG enabled.')
