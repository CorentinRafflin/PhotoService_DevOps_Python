#!/usr/bin/env python3

import logging
import json

import connexion
from connexion import NoContent
from photo import *
from mongoengine import *

from bson.objectid import ObjectId
from bson import json_util
from bson.errors import InvalidId

from flask import jsonify
import json
import flask
import robustify

@robustify.retry_mongo
def mongo_post(display_name, my_photo):
    ph = Photo(author=display_name, photo=my_photo).save()
    return ph

@robustify.retry_mongo
def mongo_get_photographer_by_name(name):
    ph = Photographer.objects(display_name=name).get()
    return ph

@robustify.retry_mongo
def mongo_get_photos(display_name):
    qs = Photo.objects(author=display_name)
    return [flask.request.url_root + "photo/" + str(ph.author) +"/" + str(ph.id)
            for ph in qs.order_by('id')]

@robustify.retry_mongo
def mongo_get_single_photo_URI(display_name,photo_id):
    qs = Photo.objects(author=display_name,id=ObjectId(photo_id))
    return [flask.request.url_root + "photo/" + str(ph.author) +"/" + str(ph.id)
            for ph in qs.order_by('id')]

@robustify.retry_mongo            
def mongo_get_single_photo(display_name, photo_id):
    ph = Photo.objects(author=display_name, id=ObjectId(photo_id)).first()
    if ph is None:
       return "Not found", 404 
    return flask.send_file(ph.photo, mimetype='image/png')

@robustify.retry_mongo
def mongo_delete_photo(display_name, photo_id):
    ph = Photo.objects(author=display_name, id=ObjectId(photo_id)).get().delete()

@robustify.retry_mongo
def mongo_get_photo_data(display_name, photo_id):
    ph = Photo.objects(author=display_name, id=ObjectId(photo_id)).get()
    return ph

@robustify.retry_mongo
def mongo_put_data(display_name, photo_id, title, location, comment, tags):
    Photo.objects(author=display_name, id=ObjectId(photo_id)).update(title = title, location = location, comment=comment, tags=tags)
    


