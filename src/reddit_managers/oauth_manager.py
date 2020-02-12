import threading
import http.server
import os
import socketserver
import urllib
import webbrowser

from logzero import logger
import praw

from core import variables

def _new_reddit_instance():
	return praw.Reddit(client_id=variables.reddit_client_id, client_secret=None, redirect_uri='http://localhost:8080', user_agent=variables.reddit_user_agent)

def _get_url(reddit_instance):
	return reddit_instance.auth.url(['creddits modcontributors modmail modconfig subscribe structuredstyles vote wikiedit mysubreddits submit modlog modposts modflair save modothers read privatemessages report identity livemanage account modtraffic wikiread edit modwiki modself history flair'], '...', 'permanent')

def authorize_new_reddit_account():
	logger.info("Starting authorization for new user")
	reddit_instance = _new_reddit_instance()
	logger.info("Opening authorization url")
	webbrowser.open(_get_url(reddit_instance))
	logger.info("Waiting for response")
	with socketserver.TCPServer(("127.0.0.1", 8080), OauthHandler) as httpd:
		httpd.serve_forever()
	if os.environ["reddit_code"] == "request_denied":
		logger.warn("Authorization request denied by user.")
		del os.environ["reddit_code"]
		return
	logger.info("Authorizating with reddit")
	token = reddit_instance.auth.authorize(os.environ["reddit_code"])
	logger.info("Authorization done. Saving token")
	users = variables.config.get("users")
	users = {**users, reddit_instance.user.me().name: token}
	variables.config.set("users", users)
	variables.config.save()
	logger.info("Token saved.")

class OauthHandler(http.server.BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html; charset=utf-8')
		self.end_headers()
		logger.info("Processing response")
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
