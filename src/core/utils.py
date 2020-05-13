"""
    This file is part of UtopiaForReddit by Accessiware.

    UtopiaForReddit is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    UtopiaForReddit is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with UtopiaForReddit.  If not, see <https://raw.githubusercontent.com/NicklasTegner/UtopiaForReddit/master/LICENSE>.
"""

import os
import time
import logging
from logging.config import dictConfig

import requests
import requests_cache

from core import variables

def insure_filesystem():
	try:
		os.makedirs(variables.data_dir)
		variables.first_run = True
	except:
		pass
	try:
		os.makedirs(os.path.join(variables.data_dir, "logs"))
	except:
		pass

def setup_logging():
	"""Setup the logging, setting the correct parsers and adjusting the log level"""
	current_time = time.strftime("%Y:%m:%d-%H:%M:%S")
	logging_config = dict(
	version = 1,
	formatters = {
		'f': {
		'format': '%(threadName)s %(levelname)-2s %(message)s | %(asctime)s',
		'datefmt': '%Y-%m-%d %H:%M'
		}
		},
	handlers = {
		'h': {'class': 'logging.StreamHandler',
			'formatter': 'f',
			'level': logging.DEBUG},
		'h2': {'class': 'logging.FileHandler',
		  'filename': os.path.join(variables.data_dir, "logs", current_time.replace(":", "_")+'.log'),
			  'formatter': 'f',
			  'level': logging.DEBUG}
		},
		root = {
		'handlers': ['h', 'h2'],
		'level': logging.DEBUG,
		},
)
	dictConfig(logging_config)

def setup_caching():
	logging.info("Installing cache")
	requests_cache.install_cache(os.path.join(variables.data_dir, 'cache'), expire_after=43200)
	logging.info("Caching installed and enabled.")
