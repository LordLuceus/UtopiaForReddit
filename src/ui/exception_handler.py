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

import wx
import wx.lib.dialogs
import textwrap
import traceback
import sys
from logzero import logger

def attach():
	sys.excepthook = _custom_excepthook

def dettach():
	sys.excepthook = sys.__excepthook__

def _custom_excepthook(exception_type, value, tb):
	dlg_content = textwrap.dedent("""\
	An unhandled exception occurred !
	
	Type : {}
	
	Message : {}
	
	Stack trace :
	{}\
	""").format(exception_type, value, ''.join(traceback.format_tb(tb)))
	logger.error(dlg_content.replace("\n\n", "\n"))
	dlg = wx.lib.dialogs.ScrolledMessageDialog(None, dlg_content, "Unhandled exception", size=(700, 500), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
	dlg.ShowModal()
	dlg.Destroy()
