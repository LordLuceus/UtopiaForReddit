import platform
from datetime import datetime

import requests_cache
from logzero import logger
import wx
import praw
from reddit_managers.stream_manager import SubredditStreamer

from ui import preferences
from ui import info_box
from ui.account_manager import *
from core import variables

class MainWindow(wx.Frame):
	def __init__(self):
		# first construct reddit instances with the found access tokens.
		users = variables.config.get("users")
		accounts = {}
		for username in users.keys():
			accounts[username] = praw.Reddit(client_id=variables.reddit_client_id, client_secret="", user_agent=variables.reddit_user_agent, refresh_token=users[username])
		super().__init__(parent=None, title="Utopia For Reddit", style=wx.MAXIMIZE)
		self.accounts = accounts
		
		application_menu= wx.Menu()
		application_menu.Append(10000, "Account Manager", "Add and remove reddit accounts.")
		application_menu.Bind(wx.EVT_MENU, self.on_open_account_manager, id=10000)
		application_menu.Append(wx.ID_PREFERENCES, "&Preferences" + "\tCTRL+SHIFT+P" if platform.system() == "Windows" else "&Preferences" + "\tCTRL+,", "Open the preferences.")
		application_menu.Bind(wx.EVT_MENU, self.on_open_preferences, id=wx.ID_PREFERENCES)
		menuBar = wx.MenuBar()
		menuBar.Append(application_menu, "Application")
		self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
		self.panel = wx.Panel(parent=self)
		self.streamers = {}
		
		self.accounts_list = wx.ListView(parent=self.panel, style=wx.LC_LIST)
		counter = 0
		for username in accounts.keys():
			counter = self.accounts_list.InsertItem (counter, username)
		self.accounts_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_account_clicked)
		self.accounts_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_account_selected)
		
		self.account_overview_list = wx.ListView(parent=self.panel, style=wx.LC_LIST)
		self.account_overview_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_feed_selected)
		
		self.feed_overview_list = wx.ListView(parent=self.panel, style=wx.LC_LIST)
		
		self.Centre()

	def on_account_clicked(self, event):
		username = event.GetLabel()
		account = self.accounts[username]
		gold_member_status = "Reddit Gold Member" if account.user.me().is_gold else "Standard Reddit Member"
		parsed_trophies = ""
		for trophy in account.user.me().trophies():
			parsed_trophies += "\n" + trophy.name
			if trophy.description is not None:
				parsed_trophies += " (" + trophy.description + ")"
			email_status = "Yes" if account.user.me().has_verified_email else "No"
		msg = f"""Username: {account.user.me()} ({gold_member_status})

Comment Karma: {account.user.me().comment_karma}
Link Karma: {account.user.me().link_karma}
Coins: {account.user.me().coins}

Email verified: {email_status}
Created: {datetime.utcfromtimestamp(account.user.me().created_utc).strftime('%Y-%m-%d %H:%M:%S')}

Trophies: {parsed_trophies}
		"""
		info_box.show_info_box(self, f"{account.user.me()} profile", msg)

	def on_account_selected(self, event):
		username = event.GetLabel()
		self.current_account = self.accounts[username]
		self.account_overview_list.ClearAll()
		self.account_overview_list.InsertItem(0, "home")
		counter = 1
		for subreddit in self.accounts[username].user.subreddits():
			self.streamers[subreddit.display_name] = SubredditStreamer(self.current_account, subreddit.display_name)
			counter = self.account_overview_list.InsertItem(counter, subreddit.display_name)

	def on_feed_selected(self, event):
		feed_name = event.GetLabel()
		self.feed_overview_list.ClearAll()
		if feed_name == "home":
			with requests_cache.disabled():
				count = 0
				for submission in self.current_account.front.hot():
					count = self.feed_overview_list.InsertItem(count, submission.title)
					if count == 250:
						break
				return
		else:
			count = 0
			submissions = self.streamers[feed_name].submissions
			count = 0
			for submission in submissions:
				count = self.feed_overview_list.InsertItem(count, submission.title)
				if count == 250:
					break

	# menubar
	def on_open_account_manager(self, event):
		self.Destroy()
		amui = AccountManagerUI(self)
		amui.Show()
		while amui.IsShownOnScreen():
			wx.YieldIfNeeded()
		main_ui = MainWindow()
		wx.GetApp().SetTopWindow(main_ui)
		main_ui.Show()

	def on_open_preferences(self, event):
		preferences.open_preferences()