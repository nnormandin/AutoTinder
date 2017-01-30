# match visualization - graph of when recently active
# show stale matches
# delete stale
# show/download pics
# sort by near you and active recently
# show photos of recent matches


import pynder, os, time
from geopy.geocoders import Nominatim


# function to start session - locates fbid and token if in cwd
def create_session(token = None, dir = None):

	# see if a directory for the fbid and token is supplied
	if dir:
		wd0 = os.getcwd()
		os.chdir(dir)
		token = open('token.txt').read()
		os.chdir(wd0)

	# see if token is supplied
	if token is None is dir is None:

		# check if it's in the working directory
		print('** searching current working directory for token')
		dirfiles = os.listdir()

		# open and read if found
		if 'token.txt' in dirfiles:
			token = open('token.txt').read()

		else:
			# suggest get_token() function
			print("** no token supplied. Use get_token() function to retrieve one")

	session = pynder.Session(token)
	user = session.profile.name
	print("** hello {0}, AutoTinder session initiated".format(user))
	return(session)

# function to retrieve matches
def get_matches(session, since = None, num_attempts = 3, summary = True):
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
			if summary:
				match_summary(matches)
			return matches
	if not matches:
		print('** could not retrieve matches')
		return

# summarize matches
def match_summary(session, matches, days = 5):

	print('\n** you have matched with {0} users'.format(len(matches)))

	since = datetime.today()-timedelta(days = days)

	# metrics
	my_id = session.profile.id
	messaged_users = [x for x in matches if x.messages]
	print('** you have talked to {0} of those users'.format(len(messaged_users)))

	you_last = sum(1 for x in messaged_users if x.messages[-1].to.id == my_id)
	them_last = len(messaged_users) - you_last
	print('** {0} of them have not responded to your last message'.format(you_last))
	print('** {0} of them messaged you last'.format(them_last))

	recent = [x for x in matches if datetime.strptime(x.user.ping_time[:10], '%Y-%m-%d') > since]
	print('** {0} of your matches have been online in the past {1} days'.format(len(recent), days))


# function to adjust radius
def adjust_radius(session, radius = 5):
	# if not _is_session(session):
	# 	raise
	cr = session.profile.distance_filter
	if cr == radius:
		print("** radius is already " + str(cr))
	else:
		print("** current radius is " + str(session.profile.distance_filter))
		session.update_profile({"distance_filter": radius})
		print("** radius adjusted to " + str(radius))


# like any user within the radius that doesn't have mutual friends
def like_nearby(session, no_mutuals = True, sleeptime = 3, limit = 1000, repeats = 1):
	print('**searching nearby')
	for i in range(0, repeats):
		limit = min(limit, 10)
		nearby = session.nearby_users(limit = limit)
		maxlikes = min(limit, len(nearby))
		print("**found " + str(len(nearby)) + " users")
		print("**analyzing " + str(maxlikes) + " users")
		for user in nearby:
			if len(user.common_connections) > 0 and no_mutuals:
				user.dislike()
				print(user.name + " had a mutual friend")
				time.sleep(sleeptime)
			else:
				print("you liked " + user.name)
				user.like()
				time.sleep(sleeptime)
		time.sleep(sleeptime)


# send message to users who meet radius / time criteria
def broadcast(matches, radius = 10, hours = 24, message = None):
	matches = [x for x in matches if not x.messages]
	since = datetime.today()-timedelta(hours = hours)

	for m in matches:
		if m.user.distance_km < radius:
			last = datetime.strptime(m.user.ping_time[:10], '%Y-%m-%d')
			if last > since:
				print('**{0} is {1}km away'.format(m.user.name, m.user.distance_km))
				msg = 'hey {0}!'.format(m.user.name)
				m.message(msg)
				time.sleep(2)
				m.message('do you want to hear a joke about ghosts?')
				time.sleep(2)


# change location
def change_location(session, location_name):
	geolocator = Nominatim()
	location = geolocator.geocode(location_name)
	print('** changing location to {0}'.format(location.address))
	session.update_location(location.latitude, location.longitude)
	print('** location changed')


# make yourself undiscoverable
def go_invisible(session):
	if session.profile.discoverable:
		session.update_profile({"discoverable": False})
	print("You are now invisible")


# make sure you're currently discoverable
def go_visible(session):
	if not session.profile.discoverable:
		session.update_profile({"discoverable": True})
		print("You have been made discoverable")
	else:
		print("You are already discoverable")

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

