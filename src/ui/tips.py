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

import wx.adv

from core import variables

class UtopiaTipProvider(wx.adv.TipProvider):
	def __init__(self, index=0):
		self.tips = [
		"When clicking on an username in the account list, information about that account will be shown."
		]
		self.index = variables.config.get("current_tip")
		super().__init__(self.index)
	
	def GetCurrentTip(self):
		return self.index
	
	def GetTip(self):
		tip = ""
		try:
			tip = self.tips[self.index]
			self.index = self.index+1
		except IndexError:
			self.index = 0
			tip = self.tips[self.index]
		finally:
			variables.config.set("current_tip", self.index)
			variables.config.save()
		return tip

def show_tips(parent, bypass=False):
	if variables.config.get("show_tips_on_startup") == False and bypass == False:
		return
	variables.config.set("show_tips_on_startup", wx.adv.ShowTip(parent, UtopiaTipProvider(), variables.config.get("show_tips_on_startup")))
	variables.config.save()
