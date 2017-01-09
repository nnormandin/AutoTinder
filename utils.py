# get matches
# report n-matches, recently active
# match visualization - graph of when recently active
# show stale matches
# number who have messaged
# number who haven't responded to last
# delete stale
# show/download pics
# sort by near you and active recently
# change location
# launch messages based on when active and distance
# (joke about ghosts default, maybe gif) -- include name?
# show photos of recent matches


import pynder, os

# function to start session - locates fbid and token if in cwd
def create_session(facebookID, token):

	# see if token is supplied
	if token is None:

		# check if it's in the working directory
		print('** searching current working directory for token')
		dirfiles = os.listdir()

		# open and read if found
		if 'token.txt' in dirfiles and 'fbid.txt' in dirfiles:
			facebookID = open('fbid.txt').read()
			token = open('token.txt').read()

		# suggest get_token() function
		print("** no token supplied. Use get_token() function to retrieve one")
	
	session = pynder.Session(facebookID, token)
	user = session.profile.name
	print("** hello {0}, AutoTinder session initiated".format(user))
	return(session)

# function to retrieve matches
def get_matches(session, since = None, num_attempts = 3):
	matches = []
	for i in range(1, num_attempts):
		if not matches:
			try:
				matches = session.matches(since = since)
			except:
				print('** attempt number {0} failed.'.format(i))
				print('** attempting {0} more times'.format(num_attempts - i))
		else:
			print('** located {0} matches'.format(len(matches)))
			return matches
	if not matches:
		print('** could not retrieve matches')
		return



# function to adjust radius
def adjust_radius(session, radius = 5):
	if not _is_session(session):
		raise
	cr = session.profile.distance_filter
	if cr == radius:
		print("**radius is already " + str(cr))
	else:
		print("**current radius is " + str(session.profile.distance_filter))
		session.update_profile({"distance_filter": radius})
		print("**radius adjusted to " + str(radius))


# like any user within the radius that doesn't have mutual friends
def like_friendless(session, sleeptime=3, limit=1000):
	try:
		limit = min(limit, 10)
		nearby = session.nearby_users(limit = limit)
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
def go_invisible(session):
	if session.profile.discoverable:
		session.update_profile({"discoverable": False})
		print("** you are now invisible")
	else:
		print("** you are already invisible")


# make sure you're currently discoverable
def go_visible(session):
	if not session.profile.discoverable:
		session.update_profile({"discoverable": True})
		print("** you have been made discoverable")
	else:
		print("** you are already discoverable")

# def _is_session(x):
# 	if type(x) not "Session":
# 		print("Please use a valid Session object")
# 		return(False)
# 	else:
# 		return(True)

# example steps
if __name__ == "__main__":

	# move to project directory
	os.chdir('/home/nick/python/projects/AutoTinder/')

	# load facebook ID and auth token
	token = open('token.txt').read().strip()
	fbid = open('fbid.txt').read().strip()

	# create session
	session = create_session(fbid, token)
	adjust_radius(session, radius = 20)
	#for i in range(0, 50): like_friendless()
	#time.sleep(5)
	adjust_radius(session, radius = 5)
	go_invisible(session)

