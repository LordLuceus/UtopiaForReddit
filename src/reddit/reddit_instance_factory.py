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

import praw

from core import variables

def new_reddit_instance(token=None):
	if token is None:
		return praw.Reddit(client_id=variables.reddit_client_id, client_secret=None, redirect_uri='http://localhost:8080', user_agent=variables.reddit_user_agent)
	else:
		return praw.Reddit(client_id=variables.reddit_client_id, client_secret=None, refresh_token=token, redirect_uri='http://localhost:8080', user_agent=variables.reddit_user_agent)
