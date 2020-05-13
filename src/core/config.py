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

import logging
import pickle
import sys
import os
import lzma
from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
from Cryptodome import Random
from core import variables

# internal variables
compression_level = 6

# Internal functions.
def encrypt_data(key, data):
	try:
		key = key.encode("utf-8")
	except AttributeError:
		pass
	try:
		data = data.encode("utf-8")
	except AttributeError:
		pass
	# Hashing key with SHA256 entirely alleviates the need for any padding.
	key = SHA256.new(key).digest()
	encryptor = AES.new(key, AES.MODE_CFB)
	data = encryptor.encrypt(data)
	return encryptor.iv + data


def decrypt_data(key, data):
	try:
		key = key.encode("utf-8")
	except AttributeError:
		pass
	# Hashing key with SHA256 entirely alleviates the need for any padding.
	key = SHA256.new(key).digest()
	iv = data[:16]
	data = data[16:]
	decryptor = AES.new(key, AES.MODE_CFB, iv)
	decryptedData = decryptor.decrypt(data)
	return decryptedData

def compress_data(data):
	return lzma.compress(data, preset=compression_level)

def decompress_data(data):
	return lzma.decompress(data)

class Config():
	def __init__(self, file, password, defaults=None):
		self.file = file
		self.password = password
		self.defaults = defaults
		self.data = {}

	def load(self):
		try:
			f = open(self.file, "rb")
			data = f.read()
			f.close()
			dData = decrypt_data(self.password, data)
			cData = decompress_data(dData)
			self.data = pickle.loads(cData)
			return self
		except FileNotFoundError:
			f = open(self.file, "wb")
			f.close()
			return self
		except lzma.LZMAError:
			return self

	def save(self):
		pData = pickle.dumps(self.data)
		cData = compress_data(pData)
		eData = encrypt_data(self.password, cData)
		f = open(self.file, "wb")
		f.write(eData)
		f.close()
		return self

	def save_defaults(self):
		for key in self.defaults:
			if key in self.data:
				continue
			self.data[key] = self.defaults[key]
		self.save()
		return self

	def get(self, key):
		if key in self.data:
			return self.data[key]
		else:
			if self.defaults == None:
				raise ValueError("Key not found in configuration and no defaults are specified")
				return None
			else:
				if key in self.defaults:
					return self.defaults[key]
				else:
					raise ValueError("Key not in config and key not in default.")
					return None

	def set(self, key, value):
		if "memory" not in key or "secret" not in key:
			logging.debug(f"Config: Setting {key} to {value}.")
		self.data[key] = value
		return self

# Get the global configuration instance.
def get_config():
	return Config(os.path.join(variables.data_dir, "application.conf"), "jsdiasjd89j8)HD78shs7(DH7sa8dh", variables.defaults)
