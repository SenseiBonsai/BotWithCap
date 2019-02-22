#import _thread
import time
import json

import urllib.request

from config import *
from alerts import add_alert

def yt(command):
	# compare the subscriber-counts of PewDiePie and T-Series
	if command[0] == "king":
		return compare("PewDiePie", "TSeries")

	# compare the subscriber-counts of two YouTube-channels
	if len(command) == 3 and command[0] == "compare":
		return compare(command[1], command[2])

	if len(command) >= 3 and command[0] == "alert":
		return alert(command)

	# get the subscriber-count of one YouTube-channel
	else:
		subs = get_subs(command[0])
		if subs == -1:
			return "Couldn't get the subscriber-count for the channel " + command[0]
		return command[0] + " has " + "{:,d}".format(int(subs)) + " subscribers."

	return 'Unknown command\nUse /yt_help to get some advice'


# call to compare the subscriber-counts of user_a and user_b
def compare(user_a, user_b):
	subs_a = get_subs(user_a)
	subs_b = get_subs(user_b)

	if subs_a == -1:
		return "Couldn't get the subscriber-count for the channel " + user_a
	if subs_b == -1:
		return "Couldn't get the subscriber-count for the channel " + user_b

	if subs_a >= subs_b:
		subs_difference = subs_a - subs_b
		return user_a + " has " + "{:,d}".format(subs_a) + " subscribers.\n" + user_b + " has " + "{:,d}".format(subs_b) + " subscribers.\n" + user_a + " is " + "{:,d}".format(subs_difference) + " subscribers ahead."
	else:
		subs_difference = subs_b - subs_a
		return user_b + " has " + "{:,d}".format(subs_b) + " subscribers.\n" + user_a + " has " + "{:,d}".format(subs_a) + " subscribers.\n" + user_b + " is " + "{:,d}".format(subs_difference) + " subscribers ahead."

# gets the subscriber-count of one YouTube-channel
def get_subs(name):
	try:
		data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=" + name + "&key=" + google_api_key).read()
		subs = json.loads(data.decode('utf-8'))["items"][0]["statistics"]["subscriberCount"]

		return int(subs)
	except:
		return -1

def alert(command):
	# compares two channels and alerts you, when a gets more subscribers than b
	if len(command) == 4 and command[1] == "compare":
		user_a = command[2]
		user_b = command[3]
		command.append("yt")
		add_alert(command)
		return ("I will alert you, when " + user_a + " gets more subscribers than " + user_b)

	# alerts you when a channel passes a milestone
	if len(command) == 4 and command[1] == "milestone":
		user = command[3]
		subs = get_subs(user)
		try:
			subcount_milestone = int(command[2])
		except:
			return ("You entered an invalid milestone")
		milestone = subs - (subs % subcount_milestone) + subcount_milestone
		milestone = str(milestone)
		command.append(milestone)
		command.append("yt")
		add_alert(command)
		return ("I will alert you, when " + user + " passes {:,d}".format(int(milestone)) + " subscribers")

	# alerts you when the subgap between two channels falls under a value
	if len(command) == 5 and command[1] == 'subgap':
		user_a = command[2]
		user_b = command[3]
		subgap = command[4]
		subs_a = get_subs(user_a)
		subs_b = get_subs(user_b)
		if (subs_a == -1):
			return "Couldn't get the subriber-count for the channel " + user_a
		if (subs_b == -1):
			return "Couldn't get the subriber-count for the channel " + user_b
		command.append('yt')
		add_alert(command)
		return ("I will alert you, when the subgap between " + user_a + " and " + user_b + " falls below " + subgap)

	return "Unknown command"


def alert_compare(user_a, user_b):
	subs_a = get_subs(user_a)
	subs_b = get_subs(user_b)

	if subs_a == -1:
		return "Couldn't get the subscriber-count for the channel " + user_a
	if subs_b == -1:
		return "Couldn't get the subscriber-count for the channel " + user_b

	if subs_a >= subs_b:
		subs_difference = subs_a - subs_b
		return user_a + " has now {:,d}".format(subs_difference) + " more subs than " + user_b
	else:
		return None

def alert_milestone(subcount_milestone, user, milestone):
	subcount_milestone = int(subcount_milestone)
	subs = get_subs(user)

	if subs == -1:
		return "Couldn't get the subscriber-count for the channel " + user

	milestone = int(milestone)
	if subs > milestone:
		next_milestone = subs - (subs % subcount_milestone) + subcount_milestone
		new_alert = ['yt', 'alert', 'milestone', str(subcount_milestone), user, str(next_milestone)]
		new_alert.append(user + " has now {:,d}".format(milestone) + " subscribers")
		return new_alert


def alert_subgap(user_a, user_b, subgap):
	subs_a = get_subs(user_a)
	subs_b = get_subs(user_b)

	if subs_a == -1:
		return "Couldn't get the subscriber-count for the channel " + user_a
	if subs_b == -1:
		return "Couldn't get the subscriber-count for the channel " + user_b

	if subs_a >= subs_b:
		subs_difference = subs_a - subs_b
	else:
		subs_difference = subs_b - subs_a

	if subs_difference < int(subgap):
		return "The subgap between " + user_a + " and " + user_b + " fell below " + subgap + ". It's currently at {}".format(subs_difference)