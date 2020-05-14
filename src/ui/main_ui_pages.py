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

import wx
from wxasync import *

from core import variables

class GenericNotebookPanel(wx.Panel):
	def __init__(self, parent, reddit_instance):
		super().__init__(parent)
		self.reddit_instance = reddit_instance
		self.shown = False

	async def on_gain_focus(self):
		pass

	async def on_lost_focus(self):
		pass

class HomePanel(GenericNotebookPanel):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.submission_list = wx.ListView(self)
		self.submission_list.AppendColumn("HOME")
		
	async def on_gain_focus(self):
		self.shown = True
		StartCoroutine(self._stream_home_feed(), self.submission_list)
	
		async def on_lost_focus(self):
			self.shown = False
			# clean the items
			self.submission_list.ClearAll()
			return
			if self.submission_list.GetItemCount() <= 100:
				return
			while self.submission_list.GetItemCount() <= 100:
				self.submission_list.DeleteItem(self.submission_list.GetItemCount()-1)
			
	
	async def _stream_home_feed(self):
		while self.shown:
			# ok, we actually cheating here, because the home / front doesn't have methods for streaming, so we grab the all subreddit instead.
			for submission in self.reddit_instance.subreddit('all').stream.submissions():
				self.submission_list.InsertItem(0, submission.title)
				await asyncio.sleep(1)

class SubredditsPanel(GenericNotebookPanel):
	def __init__(self, parent, reddit_instance):
		super().__init__(parent, reddit_instance)
		self.subreddit_list = wx.ListView(self)
		self.subreddit_list.AppendColumn("Subreddits")

	async def on_gain_focus(self):
		count = 0
		for subreddit in sorted(self.reddit_instance.user.subreddits(), key=lambda subreddit: subreddit.display_name):
			count = self.subreddit_list.InsertItem(count, subreddit.display_name)+1

	async def on_lost_focus(self):
		pass

class ProfilePanel(GenericNotebookPanel):
	async def on_gain_focus(self):
		pass
	
		async def on_lost_focus(self):
			pass

