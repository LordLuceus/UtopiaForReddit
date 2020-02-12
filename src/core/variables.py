from appdirs import user_data_dir

from core.version_helper import git_tag_version, git_tag_release_channel

app_name = "UtopiaForReddit"
app_author = "accessiware"
version = git_tag_version
release_channel = git_tag_release_channel
data_dir = user_data_dir(app_name, app_author, roaming=True)

# Configuration singleton
config = None
defaults = {"users": {}, "auto_check_for_updates": True}

# reddit api stuff.
reddit_client_id = 'TkSJQnpaTrTtSQ'
reddit_user_agent = 'UtopiaForReddit by /u/UtopiaForReddit'

# updater stuff
update_in_progress = False
