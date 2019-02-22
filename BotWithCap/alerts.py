import os

alerts_filepath = str(os.path.abspath(os.path.dirname(__file__))) + '/alerts.txt'

def alerts(command):
	# list all alerts
	if command[0] == 'list':
		return show_alerts()

	# remove an alert
	if command[0] == 'remove':
		return remove_alert(int(command[1]))

	else:
		return 'Unknown command\nUse /alert_help to get some advice'


def add_alert(command):
	# open alert-file
	try:
		f = open(alerts_filepath, 'a')
	except:
		# debugging-message
		#print('add_alert() Could not open the file alerts.txt')
		return 0

	# build new line
	alert = command.pop()
	while len(command) > 0:
		alert = alert + " " + command.pop(0)

	f.write(alert + '\n')
	f.close()
	# debugging message
	#print('Added alert ' + alert + ' to the alerts-file')
	return 1


def get_alerts():
	try:
		with open(alerts_filepath, "r") as f:
			alerts = []
			for line in f:
				line = line.rstrip()
				alerts.append(line)
		f.close()
		return alerts
	except:
		# debugging-message
		print('get_alerts()	Could not open the file alerts.txt')
		return None

	# print numer of found alerts for debugging
	#print('Found {}'.format(len(alerts)) + ' alerts')
	return 


def check_alert(command):
	command_array = command.split(' ')
	if command_array[0] == 'yt':
		if command_array[2] == 'compare':
			from yt import alert_compare
			message = alert_compare(command_array[3], command_array[4])

		elif command_array[2] == 'milestone':
			from yt import alert_milestone
			message = alert_milestone(command_array[3], command_array[4], command_array[5])

		elif command_array[2] == 'subgap':
			from yt import alert_subgap
			message = alert_subgap(command_array[3], command_array[4], command_array[5])

		# check if the message is an error-message
		# don't send error messages for alerts
		if type(message) == str and message != None:
			if message.startswith("Couldn't get the subscriber-count for the channel "):
				return None
		
		return message

	return None

def reset_alerts(new_alerts):
	if os.path.exists(alerts_filepath):
		os.remove(alerts_filepath)

	for alert in new_alerts:
		alert = alert.split(' ')
		praefix = alert.pop(0)
		alert.append(praefix)
		add_alert(alert)

	return


def show_alerts():
	alerts = get_alerts()
	if alerts != None:
		message = '1. ' + alerts.pop(0) + '\n'
		counter = 2
		while len(alerts) > 0:
			message = message + str(counter) + '. ' + alerts.pop(0) + '\n'
			counter += 1
		message = message + 'Use /alerts remove and one of the numbers above in order to delete the corresponding alert'
		return message
	return 'There are no alerts'


def remove_alert(alert_number):
	alerts = get_alerts()
	if alert_number >= 1 and alert_number <= len(alerts):
		alert = alerts.pop(alert_number - 1)
		reset_alerts(alerts)
		return 'The alert ' + alert + ' has been removed'
	else:
		return 'Could not find an alert with that number.\nUse /alerts in order to get a list of all the alerts'