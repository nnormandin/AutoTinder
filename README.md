## AutoTinder

AutoTinder is a python submodule used to put Tinder on autopilot. It extends the [pynder](http://bit.ly/2iAVQg1) library of Tinder API calls written in python. The result is a set of convenience functions that allows you to easily automate and improve your experience.



## What can it do?

Tinder is great, but you shouldn't waste all day swiping when you can have someone else do it for you. AutoTinder chunks together the awesome basic functionality provided by `pynder` and lets you string together basic workflows with just a few lines of code.

* Initialize a Tinder session from the comfort of your computer
* Generate an authorization token if necessary
* Change location based on location name/address via geocoding
* Make yourself discoverable / undiscoverable
* Adjust your radius
* Like users around you (exclude those with mutual friends, if desired)
* Generate a summary of your matches and message history
* Send personalized messages to some of your matches based on last time online and current distance
* Loop through and respond to all recent unanswered messages

In addition to all of this great stuff, all of the functions and classes originally included in `pynder` remain intact. You can check them out [here](http://bit.ly/2iAVQg1).

## Example

```python
# import the module
import pynder

# retrieve authorization from Facebook
token = pynder.get_token(email, password)

# initiate session
s = pynder.create_session(token)

# check out your matches so far this year
matches = pynder.get_matches(s, since = '01-01-2017', summary = False)

# get some useful metrics on your match interactions
pynder.match_summary(s, matches)

# check for users near you and like them all
# unless they have mutual friends- repeat 10 times!
pynder.like_nearby(s, repeats = 10)

# change your radius to 100km, change location to NYC
pynder.change_location(s, "New York City")
pynder.adjust_radius(s, radius = 100)

# send 'hi' to all of your matches that have been
# online in the past 2 hours and are less than 10km away
pynder.broadcast(matches, radius = 10, hours = 2, message = 'hi')

# make your profile invisible
pynder.go_invisible(s)

```

## What's next?

* Send alerts with new matches and conversations
* Facial detection methods
* Delete stale / old conversations automatically
