What is Meetupslides?
=====================

Meetupslides is a web app that facilitates sharing of presentations in software meetups.


Where can I see it?
===================
http://meetupslides.com


Tell me more
============
A lot of experts present awesome stuff at meetups. The slides are usually not shared with the users. Meetupslides tries to solve this problem. Users can upload their presentations, source code, links, contact info. Users will be able to search for various presentations and access them easily.


Contributing to this repo
=========================

This is an interesting application built using Flask (an awesome python micro framework), Redis, Twitter bootstrap, amazon S3 and is hosted on heroku.

Who can contribute?
===================
  * Anyone
  * Developers interested in working/learning with python, Flask
  * Front end engineers who want to play with twitter bootstrap
  * Graphic designers

Ensure you have python, pip, virtualenv, redis installed on your machine.

    $ which python
    $ which pip
    $ which mkvirtualenv
    $ which redis-server

Installing redis:
http://redis.io/download

    $ mkvirtualenv meetupslides
    $ git clone git@github.com:teraom/meetupslides.git
    $ cd meetupslides
    $ pip install -r requirements.txt

You may want to run redis server on a different tab.
    
    $ redis-server 

To run the application
    
    $ python app.py

If you need help with getting the dev environment up and running, please feel free to contact me via github.

