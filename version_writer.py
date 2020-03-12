import sys

from justupdate.repo.version import Version

if len(sys.argv) == 1:
	print("Usage: version_writer.py version")
	sys.exit(1)

print("Starting version writer for UtopiaForReddit.")
print("Version: {}.".format(sys.argv[1]))
version = Version(sys.argv[1])
channel = ""
if version.is_stable:
	channel = "stable"
if version.is_beta:
	channel = "beta"
if version.is_alpha:
	channel = "alpha"

if channel == "":
	raise ValueError("Unable to determine release channel.")
	sys.exit(2)

print("Release channel: {}.".format(channel))

print("Writing version_helper.py in \"src/core/version_helper.py\".")
f = open("src/core/version_helper.py", "w")
f.write('git_tag_version = "{0}"\ngit_tag_release_channel = "{1}"'.format(sys.argv[1], channel))
f.close()
print("Done writing version_helper.py")
print("Version writer done")
sys.exit(0)
