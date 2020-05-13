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

import wx
from wxasync import *

from reddit import account_manager
from reddit import oauth

from ui import main_ui

class AccountManager(wx.Frame):
	def __init__(self, passthrough=False):
		super().__init__(None, title="Account Manager")
		self.Bind(wx.EVT_CLOSE, self.on_close)
		self._create(passthrough)

	def _create(self, passthrough):
		self.account_manager_backend = account_manager.AccountManager()
		self.selected_account = None
		# if passthrough is true, check if we only have one account authorizated. If we do, and passthrough is set to true, just pass control to the main ui.
		if passthrough:
			if self.account_manager_backend.amount() == 1:
				self.selected_account = self.account_manager_backend.get_usernames()[0]
				self.Close() # trigger the main ui to open
				return
		
		self.panel = wx.Panel(self, size=(400,650))
		
		self.account_list = wx.ListView(parent=self.panel, style=wx.LC_LIST)
		self._populate_account_list()
		
		self.auth_button = wx.Button(parent=self.panel, label="Authorize new account")
		AsyncBind(wx.EVT_BUTTON, self.on_auth_new_account_request, self.auth_button)
		self.delete_button = wx.Button(parent=self.panel, label="Delete")
		AsyncBind(wx.EVT_BUTTON, self.on_delete_account_request, self.delete_button)
		self.done_button = wx.Button(parent=self.panel, label="Close")
		self.done_button.Bind(wx.EVT_BUTTON, self.on_done)
		self.account_list.Bind(wx.EVT_LIST_ITEM_SELECTED, lambda event: self.done_button.SetLabel("Enter"))
		self.account_list.Bind(wx.EVT_LIST_ITEM_DESELECTED, lambda event: self.done_button.SetLabel("Close"))
		
		self.Centre()
		
		mainsizer = wx.BoxSizer(wx.VERTICAL)
		listsizer = wx.BoxSizer()
		buttonsizer = wx.BoxSizer()
		listsizer.Add(self.account_list, 0, wx.EXPAND)
		buttonsizer.Add(self.auth_button, 0)
		buttonsizer.Add(self.delete_button, 0)
		buttonsizer.Add(self.done_button, 0)
		mainsizer.Add(listsizer, 1)
		mainsizer.Add(buttonsizer, 0)
		mainsizer.Fit(self)
		
		self.Show()

	def _populate_account_list(self):
		self.account_list.ClearAll()
		counter = 0
		for username in self.account_manager_backend.get_usernames():
			counter = self.account_list.InsertItem (counter, username)

	async def on_auth_new_account_request(self, event):
		dlg = wx.MessageDialog(parent=self, caption="Authorize New Account", message="The request to authorize your Reddit account will be opened in your browser. You only need to do this once. Would you like to continue?", style=wx.YES_NO|wx.YES_DEFAULT)
		result = dlg.ShowModal()
		if result == wx.ID_NO:
			return
		oauth.authorize_new_reddit_account()
		self._populate_account_list()

	async def on_delete_account_request(self, event):
		selected = self.account_list.GetFocusedItem()
		if selected == -1:
			return
		label = self.account_list.GetItemText(selected)
		dialog = wx.MessageDialog(parent=self, caption="Confirmation", message=f"This action will remove the authorization and all stored data for the account {label} from this computer. Are you sure?", style=wx.YES_NO|wx.NO_DEFAULT|wx.ICON_WARNING)
		result = dialog.ShowModal()
		dialog.Destroy()
		if result == wx.ID_NO:
			return
		result = self.account_manager_backend.delete_account(label)
		if result == True:
			self.account_list.DeleteItem(selected)
			dialog = wx.MessageDialog(parent=self, caption="Success", message=f"Authorization and all data for {label} removed.", style=wx.OK|wx.ICON_INFORMATION)
			dialog.ShowModal()
			dialog.Destroy()
			return
		dialog = wx.MessageDialog(parent=self, caption="Error", message=f"Something went wrong when deleting the information for {label}.", style=wx.OK|wx.ICON_ERROR)
		dialog.ShowModal()
		dialog.Destroy()

	def on_done(self, event):
		selected = self.account_list.GetFocusedItem()
		if selected == -1:
			sys.exit(0)
		label = self.account_list.GetItemText(selected)
		self.selected_account = label
		self.Close()

	def on_close(self, event):
		if self.selected_account is not None:
			frame = main_ui.MainFrame(self.selected_account, self.account_manager_backend.get_token_for_username(self.selected_account))
			wx.GetApp().SetTopWindow(frame)
			frame.Show()
		event.Skip()
