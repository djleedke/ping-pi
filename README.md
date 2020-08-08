# Ping Pi

PingPi is a small application that allows you to schedule pings to websites of your choosing via a web interface.  It was created as a work around to Heroku's sleeping dynos.  Since the websites go to sleep after a half hour of non-use I needed a way to wake my sites at certain times, or to keep it up if I wanted it to be up all the time.  

Prior to this I was utilizing [Kaffeine](https://kaffeine.herokuapp.com/) which was great but only allows you to ping the a site every 30 minutes.  This wastes dyno hours as the site is up the majority of the day.  In my case I only needed my site, [TweetryDish](http://tweetry-dish-app.herokuapp.com/), to be awake at 7pm each day to fire off a scheduled tweet and that was it.  This app allows me to do that.

The Pi in PingPi is because the app is intended to be run on a Raspberry Pi, though you could definitely run it on other systems if you wish.  I use my Raspberry Pi to run the site over my local network, and then can access it via other computers on the network.  This way I don't need my main desktop to be on 24/7 to keep the pings going.

## Contents

- [Features](#Features)
- [Setup](#Setup)
- [Built With](#built-with)
- [Acknowledgements](#acknowledgements)

## Features

- Ability to schedule website pings at certain intervals or at a certain time each day
- Countdown timer so you can see when the next ping will take place

## Setup

These are instuctions to get the application up and running on a Raspberry Pi which uses a Linux operating system.  You could absolutely run it on other operating systems but a few of the commands could vary slightly.



## Built With

- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - for the webserver
- [Bootstrap](https://getbootstrap.com/docs/4.0/getting-started/introduction/) - for quick and easy responsive CSS & Javascript
- [SQLAlchemy](https://www.sqlalchemy.org/) - for handling the database
- [APScheduler](https://apscheduler.readthedocs.io/en/stable/) - for scheduling the pings
- [easytimer.js](https://github.com/albert-gonzalez/easytimer.js/) - for the countdown timers
- [Raspberry Pi](https://www.raspberrypi.org/) - for deployment

## Acknowledgements

The idea for this app was inspired by [Kaffeine](https://kaffeine.herokuapp.com/) which also lets you schedule website pings.