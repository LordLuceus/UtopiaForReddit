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
			for submission in subreddit.stream.submissions():
				self.submissions.append(submission)
	
	def get_submissions(self):
		return self.submissions

