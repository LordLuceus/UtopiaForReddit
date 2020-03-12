import wx
import wx.lib.dialogs
import textwrap

def show_info_box(parent, title, message):
	dlg_content = textwrap.dedent(message)
	dlg = wx.lib.dialogs.ScrolledMessageDialog(parent, dlg_content, title, size=(700, 500), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
	dlg.ShowModal()
	dlg.Destroy()
