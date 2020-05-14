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
import webbrowser

import wx
import wx.adv
from wxasync import AsyncBind, StartCoroutine

from reddit import reddit_instance_factory

from ui import account_manager
from ui import main_ui_pages
from ui import tips
from ui import preferences

from updater import updater

class CustomIDS:
	ACCOUNT_MANAGER = 10000
	LICENSE = 10001
	DONATE = 10002
	SHOW_TIPS = 10003
	CHECK_FOR_UPDATES = 10004

class MainFrame(wx.Frame):
	def __init__(self, username, token):
		self.username = username
		# exchange the token for a praw reddit instance that is logged in.
		self.reddit_instance = reddit_instance_factory.new_reddit_instance(token)
		super().__init__(None, wx.ID_ANY, title=f"UtopiaForReddit ({self.username})", style=wx.MAXIMIZE)
		
		# menu
		application_menu= wx.Menu()
		
		application_menu.Append(CustomIDS.ACCOUNT_MANAGER, "Account Manager", "Add and remove reddit accounts.")
		application_menu.Append(wx.ID_PREFERENCES, "&Preferences" + "\tCTRL+SHIFT+P" if platform.system() == "Windows" else "&Preferences" + "\tCTRL+,", "Open the preferences.")
		application_menu.Append(wx.ID_EXIT, "Exit")
		
		application_menu.Bind(wx.EVT_MENU, self.on_show_account_manager, id=CustomIDS.ACCOUNT_MANAGER)
		application_menu.Bind(wx.EVT_MENU, self.on_show_preferences, id=wx.ID_PREFERENCES)
		application_menu.Bind(wx.EVT_MENU, lambda event: self.Close(), id=wx.ID_EXIT)
		
		help_menu= wx.Menu()
		
		help_menu.Append(CustomIDS.LICENSE, "License")
		help_menu.Append(CustomIDS.CHECK_FOR_UPDATES, "Check for updates")
		help_menu.Append(CustomIDS.DONATE, "Donate")
		help_menu.Append(CustomIDS.SHOW_TIPS, "Show Utopia Program Tips")
		
		AsyncBind(wx.EVT_MENU, updater.menu_check_for_updates, self, id=CustomIDS.CHECK_FOR_UPDATES)
		help_menu.Bind(wx.EVT_MENU, lambda event: webbrowser.open("https://accessiware.com/donate"), id=CustomIDS.DONATE)
		help_menu.Bind(wx.EVT_MENU, lambda event: tips.show_tips(self, True), id=CustomIDS.SHOW_TIPS)
		
		menuBar = wx.MenuBar()
		menuBar.Append(application_menu, "Application")
		menuBar.Append(help_menu, "&Help")
		self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
		
		self.panel = wx.Panel(self)
		self.book = wx.Notebook(self.panel, style=wx.NB_RIGHT|wx.NB_NOPAGETHEME)
		AsyncBind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_notebook_page_change, self)
		AsyncBind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.on_notebook_page_changing, self)
		
		self.book.AddPage(main_ui_pages.HomePanel(self.book, self.reddit_instance), "HOME")
		self.book.AddPage(main_ui_pages.ProfilePanel(self.book, self.reddit_instance), "My Profile")
		
		StartCoroutine(self.book.GetPage(0).on_gain_focus(), self)
		
		self.Maximize()
		
		mainsizer = wx.BoxSizer()
		mainsizer.Add(self.book, 1, wx.EXPAND)
		self.SetSizer(mainsizer)
		mainsizer.Fit(self)

	async def on_notebook_page_change(self, event):
		page = self.book.GetPage(event.GetSelection())
		await page.on_lost_focus()

	async def on_notebook_page_changing(self, event):
		page = self.book.GetPage(event.GetSelection())
		await page.on_gain_focus()

	# event handlers for menu items
	def on_show_account_manager(self, event):
		wx.CallAfter(self.Close)
		am = account_manager.AccountManager()
		am.Show()

	def on_show_preferences(self, event):
		StartCoroutine(preferences.open_preferences, self)

