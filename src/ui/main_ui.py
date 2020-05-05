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

import platform
from datetime import datetime
import webbrowser
import random

import requests_cache
from logzero import logger
import wx
import praw
import prawcore
from reddit_managers.stream_manager import SubredditStreamer

from ui import preferences
from ui import info_box
from ui.account_manager import *
from ui.submission_viewer import *
from ui import tips

from core import variables
from core import utils

class CustomIDS:
	"""Custom UI ids"""
	ACCOUNT_MANAGER = 10000
	LICENSE = 10001
	DONATE = 10002
	SHOW_TIPS = 10003

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
		
		application_menu.Append(CustomIDS.ACCOUNT_MANAGER, "Account Manager", "Add and remove reddit accounts.")
		application_menu.Append(wx.ID_PREFERENCES, "&Preferences" + "\tCTRL+SHIFT+P" if platform.system() == "Windows" else "&Preferences" + "\tCTRL+,", "Open the preferences.")
		application_menu.Append(CustomIDS.LICENSE, "License")
		application_menu.Append(CustomIDS.DONATE, "Donate")
		application_menu.Append(CustomIDS.SHOW_TIPS, "Show Utopia Program Tips")
		application_menu.Append(wx.ID_EXIT, "Exit")
		
		application_menu.Bind(wx.EVT_MENU, self.on_open_account_manager, id=CustomIDS.ACCOUNT_MANAGER)
		application_menu.Bind(wx.EVT_MENU, self.on_open_preferences, id=wx.ID_PREFERENCES)
		application_menu.Bind(wx.EVT_MENU, lambda event: info_box.show_info_box(self, "Utopia For Reddit License", variables.program_license), id=CustomIDS.LICENSE)
		application_menu.Bind(wx.EVT_MENU, lambda event: webbrowser.open("https://accessiware.com/donate"), id=CustomIDS.DONATE)
		application_menu.Bind(wx.EVT_MENU, lambda event: tips.show_tips(self, True), id=CustomIDS.SHOW_TIPS)
		application_menu.Bind(wx.EVT_MENU, lambda event: self.Close(), id=wx.ID_EXIT)
		
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
		self.account_overview_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_feed_activated)
		
		self.feed_overview_list = wx.ListView(parent=self.panel, style=wx.LC_LIST)
		self.feed_overview_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_submission_activated)
		
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

	def on_feed_activated(self, event):
		feed_name = event.GetLabel()
		if feed_name == "home":
			event.Skip()
			return
		subreddit = self.current_account.subreddit(feed_name)
		flairs = ""
		try:
			flairs = ', '.join(subreddit.flair())
		except prawcore.exceptions.Forbidden:
			pass
		msg = f"""{subreddit}
{subreddit.description}
NSFW: {'yes' if subreddit.over18 else 'no'}, {subreddit.subscribers} subscribers.

created: {datetime.utcfromtimestamp(subreddit.created_utc).strftime('%Y-%m-%d %H:%M:%S')}
"""
		info_box.show_info_box(self, f"{subreddit} Subreddit", msg)

	def on_feed_selected(self, event):
		variables.reddit_submission_id_cache.clear()
		feed_name = event.GetLabel()
		self.feed_overview_list.ClearAll()
		if feed_name == "home":
			with requests_cache.disabled():
				count = 0
				for submission in self.current_account.front.hot(limit=200):
					count = self.feed_overview_list.InsertItem(count, submission.title)
					generated_id = random.randint(1,100000)
					variables.reddit_submission_id_cache[generated_id] = submission.id
					self.feed_overview_list.SetItemData(count, generated_id)
				return
		else:
			submissions = self.streamers[feed_name].submissions
			count = 0
			for submission in submissions:
				count = self.feed_overview_list.InsertItem(count, submission.title)
				generated_id = random.randint(1,100000)
				variables.reddit_submission_id_cache[generated_id] = submission.id
				self.feed_overview_list.SetItemData(count, generated_id)

	def on_submission_activated(self, event):
		cached_id = self.feed_overview_list.GetItemData(event.GetIndex())
		viewer = SubmissionViewer(self, self.current_account.submission(id=variables.reddit_submission_id_cache[cached_id]))
		viewer.Show(True)

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