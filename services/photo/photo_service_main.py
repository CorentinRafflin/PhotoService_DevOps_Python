#!/usr/bin/env python3

import logging
import connexion
from connexion import NoContent
from mongoengine import connect



logging.basicConfig(level=logging.DEBUG)
app = connexion.FlaskApp(__name__)
app.add_api('photo_service.yml')

connect("photos", alias="default", host="127.0.0.1")
connect("photographers", alias="db_photographers", host="127.0.0.1")
# from http://coderobot.downley.net/swagger-driven-testing-in-python.html
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

if __name__ == '__main__':
    app.run(port=8090)
