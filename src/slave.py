import praw
from logzero import logger
import wx

from core import config
from core import utils
from core import variables

from ui.account_manager import *
from ui.main_ui import *

def _real_main():
	utils.insure_filesystem()
	utils.setup_logging()
	utils.setup_caching()
	logger.info(f"Starting UtopiaForReddit version 0")
	logger.info("Loading config and saving defaults if needed.")
	variables.config = config.get_config().load().save_defaults()
	logger.info("Starting ui framework")
	app = wx.App(redirect=False, useBestVisual=True)
	# see if we need to open the account manager or just the reqgular gui (account manager, if we have no accounts authorizated)
	if len(variables.config.get("users")) == 0: # no accounts authorizated. Open account manager
		logger.info("No authorizated accounts available. Opening account manager")
		amu = AccountManagerUI()
		amu.Show()
	else: # open regular gui
		logger.info("Authorizated Accounts found. Opening regular gui")
		main_ui = MainWindow()
		app.SetTopWindow(main_ui)
		main_ui.Show()
	logger.info("Entering main loop")
	app.MainLoop()
