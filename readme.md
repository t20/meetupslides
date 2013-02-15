Meetupslides is a web application (built with Flask micro framework and Redis) that facilitates sharing of presentations in software meetups.
Users can upload their presentations, source code, links, contact info. Users will be able to search for various presentations and access them easily.
Example search keywords: flask, redis, testing frameworks in web applications, caching in Django, documentation best practices.


Site: http://meetupslides.com

Contributing to this repo

Ensure you have python, pip, virtualenv, redis installed on your machine.

$ which python
$ which pip
$ which mkvirtualenv
$ which redis-server

Installing redis:
http://redis.io/download

$ mkvirtualenv meetupslides
$ cd your-workspace
$ git clone git@github.com:teraom/meetupslides.git
$ cd meetupslides
$ pip install -r requirements.txt

You may want to run this on a different tab.
$ redis-server 

To run the application
$ python app.py

If you need help with getting the dev environment up and running, please feel free to contact me via github.

