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

class SubmissionViewer(wx.Frame):
	def __init__(self, parent, submission):
		self.parent = parent
		self.submission = submission
		super().__init__(parent=self.parent, title=self.submission.title, style=wx.DEFAULT_FRAME_STYLE|wx.FRAME_FLOAT_ON_PARENT)
		self.panel = wx.Panel(parent=self, id=wx.ID_ANY)
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		if self.submission.selftext:
			self.txtctrl = wx.TextCtrl(self.panel, wx.ID_ANY, self.submission.selftext, style=wx.TE_READONLY|wx.TE_MULTILINE)
			sizer.Add(self.txtctrl, wx.SizerFlags(1).Align(wx.TOP).Expand().Border(wx.ALL, 10))
		
		self.comments_tree = wx.TreeCtrl(self.panel, wx.ID_ANY, style=wx.TR_HIDE_ROOT|wx.TR_SINGLE)
		root_id = self.comments_tree.AddRoot("Comments")
		submission.comments.replace_more(limit=None)
		for comment in submission.comments:
			self._create_comments_tree(self.comments_tree, root_id, comment)
			
			
		sizer.Add(self.comments_tree, wx.SizerFlags(1).Align(wx.TOP).Expand().Border(wx.ALL, 10))
		
		self.panel.SetSizer(sizer)
	
	def _create_comments_tree(self, treeview, root_id, comment):
		wx.YieldIfNeeded()
		root_id = treeview.AppendItem(root_id, comment.body)
		if len(comment.replies) > 0:
			for reply in comment.replies:
				return self._create_comments_tree(treeview, root_id, reply)
		return root_id
