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
import threading
import random
import time
import platform
import subprocess
import os
import zlib
import logging

from wxasync import AsyncShowDialog, AsyncBind
import wx

import requests

from justupdate.client.client import JustUpdateClient
from justupdate.repo.version import Version

from updater.client_config import ClientConfig
from core import variables

async def menu_check_for_updates(event): # called when the user pressed the check for updates menu item.
	await check_for_updates(True)

async def check_for_updates(show_result =False):
	if variables.update_in_progress:
		err = wx.MessageDialog(wx.GetTopLevelWindows()[0], caption="UtopiaForReddit Updater", message="Updater already in progress.")
		err.ShowModal()
		err.Destroy()
		return
	logging.info("Initializing updater.")
	updater_client = JustUpdateClient(ClientConfig(), variables.version, variables.config.get("update_channel"))
	if updater_client.is_post_update():
		logging.info("Running post update actions")
		updater_client.cleanup()
		updater_client.post_update_cleanup()
		return
	if variables.config.get("auto_check_for_updates") == False:
		return
	try:
		bypass_cache = False
		if variables.release_channel == "alpha":
			logging.debug("Disabling cache when checking for updates on the alpha channel.")
			bypass_cache = True
		if updater_client.update_available(bypass_cache):
			variables.update_in_progress = True
			logging.debug("Update found.")
			logging.debug("Asking user to update.")
			q = wx.MessageDialog(wx.GetTopLevelWindows()[0], "You are running version {} however version {} is available. Do you want to update UtopiaForReddit now?".format(Version(variables.version).to_human_readable(), updater_client._update_version.to_human_readable()), "UtopiaForReddit Updater", wx.YES_NO|wx.YES_DEFAULT|wx.STAY_ON_TOP)
			q.ShowModal()
			q.Destroy()
			if result == wx.ID_NO:
				variables.update_in_progress = False
				return
			# user wants to update.
			await _do_update(updater_client)
			return
		else:
			raise ValueError("No update available.")
	except (requests.exceptions.ConnectionError, ValueError, zlib.error) as e:
		logging.warn("Status when checking for updates: "+str(e))
		if show_result:
			result = wx.MessageDialog(wx.GetTopLevelWindows()[0], caption="UtopiaForReddit", message="No update found.")
			result.ShowModal()
			result.Destroy()

async def _do_update(updater_client):
	progress_bar = wx.ProgressDialog("UtopiaForReddit Updater", _("Downloading update. Please wait!"), 100, wx.GetTopLevelWindows()[0], wx.PD_APP_MODAL|wx.PD_ELAPSED_TIME|wx.PD_ESTIMATED_TIME|wx.PD_REMAINING_TIME)
	updater_client.add_callback(lambda info: update_bar(info, progress_bar))
	logging.info("Updating UtopiaForReddit.")
	t = threading.Thread(daemon=True, target=download_update, args=(updater_client, progress_bar,))
	t.start()
	progress_bar.ShowModal()

def update_bar(info, bar):
	wx.CallAfter(bar.Update, info["percentage"])

def download_update(updater_client, dialog):
	logging.info("Downloading update-package.")
	updater_client.download_update(background=True)
	while updater_client.is_downloaded() == False:
		pass
	
	logging.debug("Download done, removing progress bar.")
	wx.CallAfter(dialog.Destroy)
	
	logging.info("Applying update.")
	wx.CallAfter(_apply_update, updater_client)

def _apply_update(updater_client):
	if platform.system() == "Windows":
		logging.info("Preparing for update.")
		wx.GetTopLevelWindows()[0].Close()
		logging.info("Executing update.")
		updater_client.execute_update()
		logging.debug("Quitting UtopiaForReddit to install the update.")
		sys.exit(0)
	if platform.system() == "Darwin":
		logging.info("Executing update.")
		if updater_client.execute_update() == False:
			logging.info("Update aborted by user.")
			return
		logging.info("Restarting UtopiaForReddit.")
		wx.GetTopLevelWindows()[0].Close()
		result = subprocess.Popen(sys.executable, shell=True)
		logging.info(f"Result {result}.")
		sys.exit(0)

