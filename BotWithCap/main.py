import os
import time
import datetime
from random import randint

import telepot
from telepot.loop import MessageLoop
#import picamera

from config import *
from alerts import *
from pi import pi
from yt import yt

running = True
shutdown = False
reboot = False
mute_alerts = False
chat_id = None
alerts_filepath = str(os.path.abspath(os.path.dirname(__file__))) + '/alerts.txt'

def handle(msg):
	# get the message and the id of the chat it was sent in
    global chat_id
    chat_id = msg['chat']['id']
    command = msg['text']

    # print the command on the pi's console for debugging
    print('Got command: ' + '{}'.format(command))

    message = handle_command(command)

    send_message(message)


def send_message(message):
	global chat_id
	bot.sendMessage(chat_id, message)


def  handle_command(command):
	command_array = command.split(' ')

	# react to simple commands, that don't take variables
	if len(command_array) == 1:
		return handle_simple_command(command_array[0])

	# roll any number of dice with any number of sides and return their total
	elif command_array[0] == '/dice':
		number_dice = int(command_array[1])
		number_sides = int(command_array[2])
		sum = 0
		count = number_dice
		while count > 0:
			sum = sum + randint(1, number_sides)
			count =- 1
		if (number_dice == 1):
			return 'You rolled a ' + '{}'.format(sum)
		
		return 'The total of the dice is ' + '{}'.format(sum)

	# react to various pi-related commands, starting with '/pi'
	elif command_array[0] == '/pi':
		# system-commands
		if command == 'reboot':
			send_message("I'm going to reboot the system")
			global reboot = True

		elif command == 'shutdown':
			send_message("I'm going to shutdown the system")
			global shutdown = True
		
		else:
			return pi(command_array[1])

	# react to YouTube-related commands
	elif command_array[0] == '/yt':
		command_array.pop(0)
		return yt(command_array)

	elif command_array[0] == '/alerts':
		command_array.pop(0)
		return alerts(command_array)

	return 'Unknown command\nUse /help to get some advice'


def handle_simple_command(command):
	global mute_alerts
	# help
	if command == '/help':
		return 'Here are some commands you can use:\n/pi_help - monitor your pi\n/yt_help - monitor your favourite YouTube-channels\n/alerts_help - monitor the alerts you set\n\n/ping - simple connection-test\n/coin - throws a coin\n/dice [numberDice] [numberSides] - throws any number of dice with any number of sides and returns their total\n/end - shuts the bot down' 
	if command == '/pi_help':
		return 'Here are some commands you can use in order to monitor your RaspberryPi:\n/pi cpu - shows the CPU-usage\n/pi ram - shows the memory-usage\n/pi temperature - shows the temperature\n/pi shutdown - shuts your pi down!\n/pi reboot - reboots your pi'
	if command == '/yt_help':
		return 'Here are some commands you can use in order to monitor your favourite YouTube-channels:\n/yt [channelName] - shows you the subscriber-counts of a YouTube-channel\n/yt compare [channelA] [channelB] - compares the subscriber-counts of two channels with eachother\n/yt alert compare [channelA] [channelB] - sets up an alert, that messages you, when channelA gets more subscribers than channelB\n/yt king - compares the subscriber-counts of PewDiePie and T-Series\n'
	if command == '/alerts_help':
		return "Here are some commands you can use in order to monitor the alers you set:\n/alerts or /alerts list - lists you all alerts you set \n/alerts remove [alertNumber] - removes the corresponding alert in the alerts-list\n/mute - you won't get any alert-messages untile you unmute them\n/unmute - you will get alert-messages again"

	# end program
	if command == '/end':
		global running
		running = False
		return 'Shutting down'

	# simple connection-test
	if command == '/ping':
		return 'pong'

	# another connection-test
	elif command == '/cookie':
		return u"\U0001F36A"

	# throws a coin for you
	elif command == '/coin':
		result = randint(0,1)
		if result == 0:
			side = 'head'
		if result == 1:
			side = 'tail'
		return 'You threw ' + '{}'.format(side)

	# rolls one six sided dice
	elif command == '/dice':
		return 'You rolled a ' + '{}'.format(randint(1, 6))

	# shows the alerts that have been set
	elif command == '/alerts':
		return show_alerts()

	# mute or unmute alert-messages
	elif command == '/mute':
		mute_alerts = True
		return "Alerts are muted. You won't get any alert-messages until you use them by sending the command /unmute"
	elif command == '/unmute':
		mute_alerts = False
		return 'Unmuted the alerts. You will get alert-messages again'

	### WIP ###
#	elif command == '/photo':
#		# take a photo
#		camera=picamera.PiCamera()
#		camera.capture('./capture.jpg')
#		camera.close()
#		message = 'Captured photo at: ' + str(datetime.datetime.now())
#
#		# sends a message to the chat
#		global chat_id
#		bot.sendPhoto(chat_id=chat_id, photo=open('./capture.jpg', 'rb'))
#		return message

	else:
		return 'Unknown command\nUse /help to get some advice'


bot = telepot.Bot(access_token)

MessageLoop(bot, handle).run_as_thread()
# print start-message on the pi's console for debugging
print('I am listening ...')

alert_list = None
while running:
	if chat_id != None:
		alert_list = get_alerts()
		
		if alert_list != None and os.path.exists(alerts_filepath):
			new_alerts = []
			for alert in alert_list:
				message = check_alert(alert)
				if type(message) == str and message != None:
					if mute_alerts == False:
						send_message(message)
				elif type(message) == list and message != None:
					message2 = message.pop()
					if mute_alerts == False:
						send_message(message2)
					string = message.pop(0)
					while len(message) > 0:
						string = string + ' ' + message.pop(0)
					new_alerts.append(string)
				else:
					new_alerts.append(alert)

			reset_alerts(new_alerts)
			del new_alerts[:]

	if reboot == True:
		os.system('sudo reboot')

	if shutdown == True:
		os.system('sudo shutdown')

	time.sleep(10)
