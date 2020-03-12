import sys
import wx
import threading
import random
import time
import platform
import subprocess
import os
import requests
from logzero import logger
from justupdate.client.client import JustUpdateClient
from justupdate.repo.version import Version
from core.client_config import ClientConfig
from core import variables

def check_for_updates(show_result =False):
	if variables.update_in_progress:
		err = wx.MessageDialog(wx.GetTopLevelWindows()[0], caption="UtopiaForReddit Updater", message="Updater already in progress.")
		err.ShowModal()
		err.Destroy()
		return
	logger.info("Initializing updater.")
	updater_client = JustUpdateClient(ClientConfig(), variables.version, variables.release_channel)
	if updater_client.is_post_update():
		logger.info("Running post update actions")
		updater_client.cleanup()
		updater_client.post_update_cleanup()
		return
	if variables.config.get("auto_check_for_updates") == False:
		return
	try:
		bypass_cache = False
		if variables.release_channel == "alpha":
			logger.debug("Disabling cache when checking for updates on the alpha channel.")
			bypass_cache = True
		if updater_client.update_available(bypass_cache):
			variables.update_in_progress = True
			logger.debug("Update found.")
			logger.debug("Asking user to update.")
			q = wx.MessageDialog(wx.GetTopLevelWindows()[0], "You are running version {} however version {} is available. Do you want to update UtopiaForReddit now?".format(Version(variables.version).to_human_readable(), updater_client._update_version.to_human_readable()), "UtopiaForReddit Updater", wx.YES_NO|wx.YES_DEFAULT|wx.STAY_ON_TOP)
			result = q.ShowModal()
			q.Destroy()
			if result == wx.ID_NO:
				variables.update_in_progress = False
				return
			# user wants to update.
			_do_update(updater_client)
			return
		else:
			raise ValueError("No update available.")
	except (requests.exceptions.ConnectionError, ValueError) as e:
		logger.warn("Status when checking for updates: "+str(e))
		if show_result:
			result = wx.MessageDialog(wx.GetTopLevelWindows()[0], caption="UtopiaForReddit", message="No update found.")
			result.ShowModal()
			result.Destroy()

def _do_update(updater_client):
	progress_bar = wx.ProgressDialog("UtopiaForReddit Updater", _("Downloading update. Please wait!"), 100, wx.GetTopLevelWindows()[0], wx.PD_APP_MODAL|wx.PD_ELAPSED_TIME|wx.PD_ESTIMATED_TIME|wx.PD_REMAINING_TIME)
	updater_client.add_callback(lambda info: update_bar(info, progress_bar))
	logger.info("Updating UtopiaForReddit.")
	t = threading.Thread(daemon=True, target=download_update, args=(updater_client, progress_bar,))
	t.start()
	progress_bar.ShowModal()

def update_bar(info, bar):
	wx.CallAfter(bar.Update, info["percentage"])

def download_update(updater_client, dialog):
	logger.info("Downloading update-package.")
	updater_client.download_update(background=True)
	while updater_client.is_downloaded() == False:
		pass
	
	logger.debug("Download done, removing progress bar.")
	wx.CallAfter(dialog.Destroy)
	
	logger.info("Applying update.")
	wx.CallAfter(_apply_update, updater_client)

def _apply_update(updater_client):
	if platform.system() == "Windows":
		logger.info("Preparing for update.")
		wx.GetTopLevelWindows()[0].Close()
		logger.info("Executing update.")
		updater_client.execute_update()
		logger.debug("Quitting UtopiaForReddit to install the update.")
		sys.exit(0)
	if platform.system() == "Darwin":
		logger.info("Executing update.")
		if updater_client.execute_update() == False:
			logger.info("Update aborted by user.")
			return
		logger.info("Restarting UtopiaForReddit.")
		wx.GetTopLevelWindows()[0].Close()
		result = subprocess.Popen(sys.executable, shell=True)
		logger.info(f"Result {result}.")
		sys.exit(0)

