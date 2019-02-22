import re
import time
import json
import os
import psutil
from datetime import timedelta

def pi(command):
    # status-request-commands
    if  command == 'cpu':
        cpu_pct = psutil.cpu_percent(interval=1, percpu=False)
        message = "My CPU usage is " + "{}".format(cpu_pct) + "%"

    elif command == 'memory' or command == 'ram':
        mem = psutil.virtual_memory()
        mem_pct = mem.percent
        message = "My memory usage is " + "{}".format(mem_pct) + "%"

    elif command == 'temperature':
        tempFile = open("/sys/class/thermal/thermal_zone0/temp")
        cpu_temp = tempFile.read()
        tempFile.close()
        cpu_temp = float(cpu_temp) / 1000
        message = "My temperature is at " + "{}".format(cpu_temp) + u'\u00b0'

    elif command == 'uptime':
        try:
            f = open( "/proc/uptime" )
            contents = f.read().split()
            f.close()
        except:
            message = "Cannot open uptime file: /proc/uptime"
            return

        seconds = float(contents[0])

        # Gets the days
        days = int(seconds / 86400)
        seconds = int(seconds % 86400)
 
        # Gets the hours
        hours = int(seconds / 3600)
        seconds = int(seconds % 3600)
 
        # Gets the minutes and seconds
        minutes = int(seconds / 60)
        seconds = int(seconds % 60)
        
        # Builds up a string in the form "N days, N hours, N minutes, N seconds"
        uptime = "";
        if days > 0:
            uptime += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
        if len(uptime) > 0 or hours > 0:
            uptime += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
        if len(uptime) > 0 or minutes > 0:
            uptime += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
            uptime += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )

        message = "My uptime is " + "{}".format(uptime)
        
    else:
        message = 'Unknown command\nUse /pi_help to get some advice'

    return message;
