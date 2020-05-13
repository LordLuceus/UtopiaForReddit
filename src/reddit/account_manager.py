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

from core import variables

class AccountManagerException(ValueError):
	pass

class AccountManager:
	def __init__(self):
		self._accounts = variables.config.get("accounts")

	def is_empty(self):
		return len(self._accounts.keys()) == 0

	def get_usernames(self):
		return list(self._accounts.keys())

	def get_token_for_username(self, username):
		try:
			return self._accounts[username]
		except KeyError: # an account with the username given does not exist.
			raise AccountManagerException(f"An account with the username \"{username}\" does not exist.")
			return None

	def amount(self):
		return len(self._accounts.keys())

	def add_account(self, username, token):
		self._accounts[username] = token
		self._refresh_accounts_in_config()

	def delete_account(self, username):
		try:
			del self._accounts[username]
			return True
		except KeyError:
			return False
		finally:
			self._refresh_accounts_in_config()

	def _refresh_accounts_in_config(self):
		variables.config.set("accounts", self._accounts)
		variables.config.save()
