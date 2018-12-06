# BotWithCap

A Telegram bot, designed for the Raspberry Pi

## Getting Started

These instructions will get you a copy of the project up and running for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

If you want to use BotWithCap, you will need Python3. I developed it on Python 3.6.7.

Dependencies you have to install:
* [telepot](https://github.com/nickoala/telepot) Python framework for Telegram Bot API 
* [psutil](https://github.com/giampaolo/psutil) Cross-platform lib for process and system monitoring in Python
* [YouTube Data API](https://developers.google.com/youtube/v3/getting-started)


```
sudo pip3 install telepot
sudo pip3 install psutil
sudo pip3 install google-api-python-client
```

You will also need a Telegram account and a Google account.

### Installing

Install all dependencies and clone this repository to your Raspberry Pi.

If you now want to run BotWithCap, you first of all will need an Telegram Bot API access-token. In order to get an access-token, you have to talk to the [BotFather](https://core.telegram.org/bots/#6-botfather).
If you have got a token, insert it into the file 'config_example.py'.

Also you will need a Google API key. You can use this [wizard](https://console.developers.google.com/start/api?id=youtube) to get it. Add a new project, make sure that you choose YouTube Data API v3 and that you choose to access public data only.
Also insert this key into 'config_example.py'

If you have done this, the content of the file should sort of look like this but with your own token/key (those below won't work):

```
# Telegram Bot API access-token
access_token = "110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"

# Google API key
google_api_key = "AIzaSyDnpJsCeag_OdCvh5_ZcJs4g-MIIrSpC6w"
```

Last step is to rename 'config_example.py' to 'config.py'.

## Test it

If you want to test your API keys, start the bot on your Raspberry Pi (you can use SSH). Therefore open up the terminal, navigate to the folder, that you cloned the repository to, and run it with python3:

```
cd BotWithCap/
sudo python3 main.py
```

You should get this output:

```
I am listening ...
```

Open up Telegram and message your bot. Send him the command: /ping

The output now looks like this:

```
I am listening ...
Got command: /ping
```

And the bot should send you a message via Telegram saying "pong"

### Commands

#### Basic
* **/help** - lists most of the commands
* **/ping** - pong (a simple connection test)
* **/coin** - throws a coin
* **/dice *numberDice* *numberSides*** - throws any number of dice with any number of sides and returns their total
* **/end** - shuts the bot down

#### Pi
* **/pi_help** - lists most of the commands
* **/pi cpu** - shows the CPU-usage
* **/pi ram** - shows the memory-usage
* **/pi temperature** - shows the temperature
* **/pi shutdown** - shuts your pi down!
* **/pi reboot** - reboots your pi

#### YouTube
* **/yt *channelName*** - shows you the subscriber-counts of a YouTube-channel
* **/yt compare *channelA* *channelB*** - compares the subscriber-counts of two channels with eachother
* **/yt alert compare *channelA* *channelB*** - sets up an alert, that messages you, when channelA gets more subscribers than channelB
* **/yt king** - compares the subscriber-counts of PewDiePie and T-Series
* **/yt alert milestone *milestone* *channel*** - sets up an alert, that **repeatedly** messages you, when a channel passes a milestone (check out the examples) 

#### Alerts
* **/alerts** - lists you all alerts you set
* **/alerts list** - same as /alerts
* **/alerts remove *alertNumber*** - removes the corresponding alert in the alerts-list
* **/mute** - you won't get any alert-messages untile you unmute them
* **/unmute** - you will get alert-messages again

### Examples
* **/dice 2 20** - will roll 2 dice with 20 sides each
* **/yt alert compare TSeries PewDiePie** - the bot will send you a message, if T-Series gets more subscribers than PewDiePie
* **/yt alert milestone 1000000 PewDiePie** - the bot will send you a message everytime when PewDiePie reaches a nother one-million-milestone

## Deployment

If you install this on your Raspberry Pi, you may want your Pi to autorun the bot on startup:

Therefore run:

```
sudo nano /etc/rc.local
```

And add the following line (change filepath to your filepath):

```
python /home/pi/BotWithCap/BotWithCap/main.py &
```

## Authors

* **Lukas** - *Initial work* - [SenseiBonsai](https://github.com/SenseiBonsai)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
