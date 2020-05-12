import os
import sys

from justupdate.repo.version import Version
from justupdate.repo.metadata import MetaData

if len(sys.argv) == 1:
	print("Usage: travis_build_cleaner.py version")
	sys.exit(1)

print("Starting travis build cleaner for UtopiaForReddit.")
print("Version: {}.".format(sys.argv[1]))
new_version = Version(sys.argv[1])
channel = ""
if new_version.is_stable:
	channel = "stable"
if new_version.is_beta:
	channel = "beta"
if new_version.is_alpha:
	channel = "alpha"

if channel == "":
	raise ValueError("Unable to determine release channel.")
	sys.exit(2)

print("Release channel: {}.".format(channel))

print("Removing older versions from ju-repo/archive")

metadata = MetaData().load()

for old_version_key in metadata.keys():
	old_version = Version(old_version_key)
	if new_version.is_alpha:
		if old_version.is_alpha == False:
			continue
		if new_version == old_version: # somehow equal
			continue
		try:
			os.remove(os.path.join("ju-repo", "archive", metadata[old_version_key]["filename"]))
		except FileNotFoundError:
			pass # already deleted
	if new_version.is_beta:
		if old_version.is_beta == False:
			continue
		if new_version == old_version: # somehow equal
			continue
		try:
			os.remove(os.path.join("ju-repo", "archive", metadata[old_version_key]["filename"]))
		except FileNotFoundError:
			pass # already deleted
	if new_version.is_stable:
		if old_version.is_stable == False:
			continue
		if new_version == old_version: # somehow equal
			continue
		try:
			os.remove(os.path.join("ju-repo", "archive", metadata[old_version_key]["filename"]))
		except FileNotFoundError:
			pass # already deleted

print("Done")
sys.exit(0)

