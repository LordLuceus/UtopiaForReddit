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

import threading

import requests_cache

class SubredditStreamer():
	def __init__(self, reddit_instance, name):
		self.name = name
		self.submissions = []
		self.reddit_instance = reddit_instance
		t = threading.Thread(target=self._stream_subreddit, daemon=True)
		t.start()
	
	def _stream_subreddit(self):
		subreddit = self.reddit_instance.subreddit(self.name)
		with requests_cache.disabled():
			[self.submissions.append(submission) for submission in subreddit.stream.submissions()]
	
	def get_submissions(self):
		return self.submissions

