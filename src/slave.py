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

import asyncio
import logging
import traceback

import wx
from wxasync import WxAsyncApp, StartCoroutine

from core import config
from core import utils
from core import variables

from reddit import account_manager as account_manager_backend

from ui import account_manager
from ui import main_ui
from ui import tips

from updater import updater

def global_exception_handler(loop, context):
	msg = "an error occurred:\n"
	for key in context.keys():
		# don't print the following info, because it's useless
		if isinstance(context[key], asyncio.events.Handle):
			continue
		
		# the below stuff, is what we want.
		msg += f"{key}:\n"
		if isinstance(context[key], str):
			msg += f"{context[key]}\n\n"
			continue
		if isinstance(context[key], Exception):
			msg += f"{context[key]}\n\n"
			continue
		if isinstance(context[key], traceback.StackSummary):
			msg += "".join(context[key].format()) + "\n"
			continue
	logging.error(msg)


def _real_main():
	utils.insure_filesystem()
	utils.setup_logging()
	logging.info(f"Starting UtopiaForReddit version {variables.version_human_friendly}")
	utils.setup_caching()
	logging.info("Loading config and saving defaults if needed.")
	variables.config = config.get_config().load().save_defaults()
	logging.info("Starting ui framework")
	loop = asyncio.get_event_loop()
	loop.set_exception_handler(global_exception_handler)
	app = WxAsyncApp(loop=loop)
	loop.set_debug(True)
	am = account_manager.AccountManager(True)
	# The account manager is either shown or passed through. In either case, the show call, are done in the create method of the account manager.
	# and then the main ui will be shown.
	# check for updates
	StartCoroutine(updater.check_for_updates(), am)
	# Show program tips
	tips.show_tips(None, False)
	loop.run_until_complete(app.MainLoop())
