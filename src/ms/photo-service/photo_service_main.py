#!/usr/bin/env python3

import logging
import connexion
from connexion import NoContent
from mongoengine import connect



logging.basicConfig(level=logging.DEBUG)
app = connexion.FlaskApp(__name__)
app.add_api('photo_service.yml')

connect("photos", host="mongodb://siteRootAdmin:passw0rd@mongo1:27017,mongo2:27017,mongo3:27017/photos?authSource=admin&replicaSet=therep", alias="photos")
connect("photosIds", host="mongodb://siteRootAdmin:passw0rd@mongo1:27017,mongo2:27017,mongo3:27017/photoIds?authSource=admin&replicaSet=therep", alias="photosIds")

# from http://coderobot.downley.net/swagger-driven-testing-in-python.html
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

if __name__ == '__main__':
    app.run(port=8080)
