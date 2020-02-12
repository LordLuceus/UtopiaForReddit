from appdirs import user_data_dir

app_name = "UtopiaForReddit"
app_author = "accessiware"
data_dir = user_data_dir(app_name, app_author, roaming=True)

# Configuration singleton
config = None
defaults = {"users": {}, "auto_check_for_updates": True}

# reddit api stuff.
reddit_client_id = 'TkSJQnpaTrTtSQ'
reddit_user_agent = 'UtopiaForReddit by /u/UtopiaForReddit'
