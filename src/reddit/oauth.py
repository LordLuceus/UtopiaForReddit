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
import http.server
import os
import socketserver
import urllib
import webbrowser
import logging

import praw

from core import variables
from reddit import account_manager

def _new_reddit_instance():
	return praw.Reddit(client_id=variables.reddit_client_id, client_secret=None, redirect_uri='http://localhost:8080', user_agent=variables.reddit_user_agent)

def _get_oauth_url(reddit_instance):
	return reddit_instance.auth.url(['creddits modcontributors modmail modconfig subscribe structuredstyles vote wikiedit mysubreddits submit modlog modposts modflair save modothers read privatemessages report identity livemanage account modtraffic wikiread edit modwiki modself history flair'], '...', 'permanent')

def authorize_new_reddit_account():
	logging.info("Starting authorization for new user")
	reddit_instance = _new_reddit_instance()
	logging.info("Opening authorization url")
	webbrowser.open(_get_oauth_url(reddit_instance))
	logging.info("Waiting for response")
	with socketserver.TCPServer(("127.0.0.1", 8080), OauthHandler) as httpd:
		httpd.serve_forever()
	if os.environ["reddit_code"] == "request_denied":
		logging.warn("Authorization request denied by user.")
		del os.environ["reddit_code"]
		return
	logging.info("Authorizating with reddit")
	token = reddit_instance.auth.authorize(os.environ["reddit_code"])
	logging.info("Authorization done. Saving token")
	am = account_manager.AccountManager()
	am.add_account(reddit_instance.user.me().name, token)
	logging.info("Token saved.")

class OauthHandler(http.server.BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html; charset=utf-8')
		self.end_headers()
		logging.info("Processing response")
		query = urllib.parse.urlsplit(self.path).query
		params = urllib.parse.parse_qs(query)
		try:
			code = params["code"][0]
			os.environ["reddit_code"] = code
			self.wfile.write(bytes("authorization request done. You can now close this window and return to the application.", "utf-8"))
		except KeyError:
			os.environ["reddit_code"] = "request_denied"
			self.wfile.write(bytes("authorization request denied. You denied the authorization request. You can now close this window and return to UtopiaForReddit.", "utf-8"))
		assassin = threading.Thread(daemon=True, target=self.server.shutdown)
		assassin.start()
