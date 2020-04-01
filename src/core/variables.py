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

from appdirs import user_data_dir

from core.version_helper import git_tag_version, git_tag_release_channel

app_name = "UtopiaForReddit"
app_author = "accessiware"
version = git_tag_version
release_channel = git_tag_release_channel
data_dir = user_data_dir(app_name, app_author, roaming=True)

# Configuration singleton
config = None
defaults = {"users": {}, "auto_check_for_updates": True, "update_channel": "stable"}

# reddit api stuff.
reddit_client_id = 'Lq2gfWTeB8KVnQ'
reddit_user_agent = 'UtopiaForReddit by /u/UtopiaForReddit'

# updater stuff
update_in_progress = False
