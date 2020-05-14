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
from wxasync import AsyncBind

from core import variables

class GenericNotebookPanel(wx.Panel):
	def __init__(self, parent, reddit_instance):
		super().__init__(parent)
		self.reddit_instance = reddit_instance

	async def on_gain_focus(self):
		pass

	async def on_lost_focus(self):
		pass

class HomePanel(GenericNotebookPanel):
	async def on_gain_focus(self):
		pass
	
		async def on_lost_focus(self):
			pass

class ProfilePanel(GenericNotebookPanel):
	async def on_gain_focus(self):
		pass
	
		async def on_lost_focus(self):
			pass
