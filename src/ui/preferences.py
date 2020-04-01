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

from logzero import logger
import wx
import wx.adv

from core import variables

class Preferences(wx.adv.PropertySheetDialog):
	def __init__(self, parent, title):
		super().__init__()
		self.parent = parent
		self.title = title

	def setup(self):
		self.SetSheetStyle(wx.adv.PROPSHEET_CHOICEBOOK)
		self.Create(self.parent, wx.ID_ANY, self.title)
		return self.GetBookCtrl()

	def finalize(self):
		self.CreateButtons()
		self.LayoutDialog()

class GeneralPreferencesPage(wx.Panel):
	def __init__(self, parent, config):
		wx.Panel.__init__(self, parent)
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		self.check_for_updates = wx.CheckBox(self, wx.ID_ANY, "Automatically check for updates on startup.")
		self.check_for_updates.SetValue(config.get("auto_check_for_updates"))
		sizer.Add(self.check_for_updates, wx.SizerFlags(1).Align(wx.TOP).Expand().Border(wx.ALL, 10))
		
		l1 = wx.StaticText(self, label="Update Channel:")
		sizer.Add(l1, wx.SizerFlags(1).Align(wx.TOP).Expand().Border(wx.ALL, 1))
		self.update_channel = wx.Choice(self, choices=["stable", "beta", "alpha"])
		self.update_channel.SetSelection(self.update_channel.FindString(config.get("update_channel")))
		sizer.Add(self.update_channel, wx.SizerFlags(1).Align(wx.TOP).Expand().Border(wx.ALL, 10))
		
		self.SetSizer(sizer)

	def save(self, config):
		config.set("auto_check_for_updates", self.check_for_updates.IsChecked())
		config.set("update_channel", self.update_channel.GetString(self.update_channel.GetCurrentSelection()))

def open_preferences():
	prefFrame = Preferences(wx.GetTopLevelWindows()[0], title="Preferences")
	base = prefFrame.setup()
	
	general = GeneralPreferencesPage(base, variables.config)
	base.AddPage(general, "General", True)
	
	prefFrame.finalize()
	prefFrame.Centre()
	result = prefFrame.ShowModal ()
	if result == wx.ID_CANCEL:
		logger.debug("Not saving preferences.")
		return
	else:
		logger.info("Saving preferences")
		count = 0
		while count < base.GetPageCount():
			page = base.GetPage(count)
			logger.debug("Saving preferences on " + page.__class__.__name__)
			page.save(variables.config)
			count += 1
		variables.config.save()
		logger.info("Preferences saved")
