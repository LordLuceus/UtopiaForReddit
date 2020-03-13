import logging
import os

import requests
import requests_cache
import logzero
from logzero import logger

from core import variables

def insure_filesystem():
	try:
		os.makedirs(variables.data_dir)
	except:
		pass
	try:
		os.makedirs(os.path.join(variables.data_dir, "logs"))
	except:
		pass

def setup_logging():
	logzero.logfile(os.path.join(variables.data_dir, "logs", "application.log"), maxBytes=1e6, backupCount=3)
	formatter = logging.Formatter('%(threadName)s %(levelname)-2s %(message)s | %(asctime)s');
	logzero.formatter(formatter)

def setup_caching():
	logger.info("Installing cache")
	requests_cache.install_cache(os.path.join(variables.data_dir, 'reddit'), expire_after=43200)
	logger.info("Removing obsolete data from cache.")
	requests_cache.remove_expired_responses()
	logger.info("Caching installed and enabled.")
