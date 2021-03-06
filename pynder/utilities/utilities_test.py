# add to respond_recent
	# read bio
	# preconfigured responses
	# age / distance
	# open pic in browser?

# match visualization - graph of when recently active
# show stale matches
# delete stale
# show/download pics
# sort by near you and active recently
# show photos of recent matches


import pynder, os, time, random
from datetime import datetime
from datetime import timedelta
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
				match_summary(session, matches)
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
	print('** {0} of them have not responded to your last message'.format(them_last))
	print('** {0} of them messaged you last'.format(you_last))

	recent = [x for x in matches if datetime.strptime(x.user.ping_time[:16], '%Y-%m-%dT%H:%M') > since]
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
		nearby = session.nearby_users(limit = limit)
		maxlikes = min(limit, len(nearby))
		print("**found " + str(len(nearby)) + " users")
		print("**analyzing " + str(maxlikes) + " users")
		for user in nearby:
			if user.common_connections and no_mutuals:
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
	since = datetime.now()-timedelta(hours = hours)

	for m in matches:
		if m.user.distance_km < radius:
			last = datetime.strptime(m.user.ping_time[:16], '%Y-%m-%dT%H:%M')
			if last > since:
				print('**{0} is {1}km away'.format(m.user.name, m.user.distance_km))
				if message:
					m.message(message)
					time.sleep(random.uniform(2.5, 4.5))
				else:
					msg = 'hey {0}!'.format(m.user.name)
					m.message(msg)
					time.sleep(random.uniform(2.5, 4.5))
					m.message('how are you doing?')
					time.sleep(random.uniform(2.5, 4.5))


# convert ping_time to datetime object
def convert_date(ping_time):
	td = timedelta(hours = 5)
	date = datetime.strptime(ping_time[:16], '%Y-%m-%dT%H:%M') - td
	return(date)


# time difference
def last_online(ping_time):
	now = datetime.now()
	then = convert_date(ping_time)
	return(now - then)


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

def respond_recent(session, matches, show_last = 4):
	conversations = [x for x in matches if x.messages]
	conversations = conversations.sort(key = lambda x: x.messages[-1].sent)
	my_id = session.profile.id

	for c in conversations:
		if c.messages[-1].to.id == my_id:
			print("\n** CONVERSATION WITH {0}:**\n".format(c.user.name))
			print_messages(c.messages, show_last, my_id)
			print('\n** RESPONSE? TYPE n TO BYPASS **\n')
			response = input()
			if response == 'n':
				os.system('clear')
				continue
			else:
				c.message(response)
				os.system('clear')


def print_messages(messages, show_last, my_id):
	i = min(show_last, len(messages))
	while i > 0:
		if messages[-i].to.id == my_id:
			print(' ' * 5 + 'THEM:\n{0}\n'.format(messages[-i].body))
			i -= 1
		else:
			print(' ' * 5 + 'ME:\n{0}\n'.format(messages[-i].body))
			i -= 1
