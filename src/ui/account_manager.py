from reddit_managers import oauth_manager

import wx

from core import variables

class AccountManagerUI(wx.Frame):
	def __init__(self, parent=None):
		super().__init__(parent=None, title="Account Manager", id=wx.ID_ANY)
		self.panel = wx.Panel(parent=self)
		self.account_list = wx.ListView(parent=self.panel, style=wx.LC_LIST)
		counter = 0
		for username in variables.config.get("users").keys():
			counter = self.account_list.InsertItem (counter, username)
		
		self.auth_button = wx.Button(parent=self.panel, label="Authorize new account")
		self.auth_button.Bind(wx.EVT_BUTTON, self.on_auth_new_account_request)
		self.delete_button = wx.Button(parent=self.panel, label="Delete")
		self.delete_button.Bind(wx.EVT_BUTTON, self.on_delete_account_request)
		self.done_button = wx.Button(parent=self.panel, label="Done")
		self.done_button.Bind(wx.EVT_BUTTON, self.on_done)
		
		self.Centre()

	def on_auth_new_account_request(self, event):
		dialog = wx.MessageDialog(parent=self, caption="Authorize New Account", message="The request to authorize your Reddit account will be opened in your browser. You only need to do this once. Would you like to continue?", style=wx.YES_NO|wx.YES_DEFAULT)
		result = dialog.ShowModal()
		dialog.Destroy()
		if result == wx.ID_NO:
			return
		oauth_manager.authorize_new_reddit_account()

	def on_delete_account_request(self, event):
		selected = self.account_list.GetFocusedItem()
		if selected == -1:
			return
		label = self.account_list.GetItemText(selected)
		dialog = wx.MessageDialog(parent=self, caption="Confirmation", message=f"This action will remove the authorization and all stored data for the account {label} from this computer. Are you sure?", style=wx.YES_NO|wx.NO_DEFAULT|wx.ICON_WARNING)
		result = dialog.ShowModal()
		dialog.Destroy()
		if result == wx.ID_NO:
			return
		self.account_list.DeleteItem(selected)

	def on_done(self, event):
		if len(variables.config.get("users").keys()) == 0:
			return
		self.Close()
