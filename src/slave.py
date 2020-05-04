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

import sys

import praw
from logzero import logger
import wx

from core import config
from core import utils
from core import variables

from ui import exception_handler
from ui import tips
from ui.account_manager import *
from ui.main_ui import *
from ui import updater

def _real_main():
	"""Setup the application, initialize the ui system, check for accounts and start"""
	utils.insure_filesystem()
	utils.setup_logging()
	utils.setup_caching()
	logger.info(f"Starting UtopiaForReddit version 0")
	logger.info("Registering exception handler.")
	exception_handler.attach()
	logger.info("Loading config and saving defaults if needed.")
	variables.config = config.get_config().load().save_defaults()
	logger.info("Starting ui framework")
	app = wx.App(redirect=False, useBestVisual=True)
	# see if we need to open the account manager or just the reqgular gui (account manager, if we have no accounts authorizated)
	if len(variables.config.get("users")) == 0: # no accounts authorizated. Open account manager
		logger.info("No authorizated accounts available. Opening account manager")
		amu = AccountManagerUI()
		amu.Show()
	else: # open regular gui because we already have accounts.
		logger.info("Authorizated Accounts found. Opening regular gui")
		main_ui = MainWindow()
		app.SetTopWindow(main_ui)
		main_ui.Show()
		tips.show_tips(main_ui)
	# only check for updates, if we are running compiled
	if hasattr(sys, "frozen"):
		logger.info("Checking for updates.")
		updater.check_for_updates()
	else:
		logger.info("Skipping update check because we are running from source.")
	logger.info("Entering main loop")
	app.MainLoop()
