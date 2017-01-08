# import required modules
import os, pynder, time

# get pynder with 'pip install pynder'

# move to home directory, open token and fbid
os.chdir('/home/nick/')
token = open('token.txt').read().strip()
fbid = open('fbid.txt').read().strip()

# begin session with id and token
session = pynder.Session(fbid, token)
print("Hello " + session.profile.name + ", tinderbot session initiated")

# make sure you're currently discoverable
if not session.profile.discoverable:
	session.update_profile({"discoverable": True})
	print("You have been made discoverable")

# function to adjust radius
def adjust_radius(radius = 5):
	cr = session.profile.distance_filter
	if cr == radius:
		print("**radius is already " + str(cr))
	else:
		print("**current radius is " + str(session.profile.distance_filter))
		session.update_profile({"distance_filter": radius})
		print("**radius adjusted to " + str(radius))


# like any user within the radius that doesn't have mutual friends
def like_friendless(sleeptime=3, limit=1000):
	try:
		nearby = session.nearby_users(limit = 10)
		maxlikes = min(limit, len(nearby))
		print("**found " + str(len(nearby)) + " users")
		print("**analyzing " + str(maxlikes) + " users")
	except:
		print("Error- probably no users in radius")
		return
	for user in nearby:
		if len(user.common_connections) > 0:
			user.dislike()
			print(user.name + " had a mutual friend")
			time.sleep(sleeptime)
		else:
			print("you liked " + user.name)
			user.like()
			time.sleep(sleeptime)

# make yourself undiscoverable
def go_invisible():
	if session.profile.discoverable:
		session.update_profile({"discoverable": False})
	print("You are now invisible")


# example steps
if __name__ == "__main__":
	#adjust_radius(20)
	#for i in range(0, 50): like_friendless()
	#time.sleep(5)
	adjust_radius(5)
	go_invisible()
