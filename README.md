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

In addition to all of this great stuff, all of the functions and classes originally included in `pynder` remain intact. You can check them out [here](http://bit.ly/2iAVQg1).

## What's next?

* Send alerts with new matches and conversations
* Facial detection and scoring methods
* Delete stale / old conversations automatically
