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
import pymongo
from flask import jsonify
import json
import flask
import ast

from photo_mongo_wrapper import *

# See:
# https://devops.com/pymongo-pointers-make-robust-highly-available-mongo-queries
# for Robust Mongo Queries

def post_photo(display_name, photo):
    try:                 
        photographer = mongo_get_photographer_by_name(display_name)
        ph = mongo_post(display_name, photo)                    
        return 'Created', 201, {'location': '/photo/' + str(ph.author) + '/' + str(ph.id) } 
    except (Photographer.DoesNotExist, InvalidId) as e:
        return 'Not Found', 404                                                                                                                     
    except pymongo.errors.ServerSelectionTimeoutError as sste:                  
        return 'Mongo unavailable', 503  
            
def get_photographer(display_name):
    logging.debug('Getting photographer with name: ' + display_name)
    try:
        ph = mongo_get_photographer_by_name(display_name)
        ph._data.pop('id') # This is not very clean ...
    except (Photographer.DoesNotExist, InvalidId) as e:
        return 'Not Found', 404
    except pymongo.errors.ServerSelectionTimeoutError as sste:
        return 'Mongo unavailable', 503
    return json.loads(json.dumps(ph._data, indent=4, default=json_util.default))
 
def get_photos(display_name):
    logging.debug('Getting photos with author: ' + display_name)
    try:
        ids = mongo_get_photos(display_name)
    except pymongo.errors.ServerSelectionTimeoutError as sste:
        return 503
    return json.loads(json.dumps(ids)) 


def get_single_photo_URI(display_name, photo_id):
    try:
        id_photo = mongo_get_single_photo(display_name, photo_id)   
    except (Photo.DoesNotExist, InvalidId) as e:
        return 'Not Found', 404
    except pymongo.errors.ServerSelectionTimeoutError as sste:
        return 503
    return json.loads(json.dumps(id_photo))[0]

def get_single_photo(display_name, photo_id):
    try:
        photo = mongo_get_single_photo(display_name, photo_id)
    except pymongo.errors.ServerSelectionTimeoutError as sste:
        return 503
    return photo

def delete_photo(display_name, photo_id):
    try:  
        mongo_delete_photo(display_name, photo_id)
        return 'Deleted', 204
    except (Photo.DoesNotExist, InvalidId) as e:
        return 'Not Found', 404
    except pymongo.errors.ServerSelectionTimeoutError as sste:                  
        return 'Mongo unavailable', 503  

def get_photo_data(display_name, photo_id):
    try:
        ph = mongo_get_photo_data(display_name, photo_id)
        ph._data.pop('photo')
        ph._data.pop('id')
    except (Photo.DoesNotExist, InvalidId) as e:
        return 'Not Found', 404
    except pymongo.errors.ServerSelectionTimeoutError as sste:
        return 'Mongo unavailable', 503
    return json.loads(json.dumps(ph._data, indent=4, default=json_util.default))


def put_photo_data(display_name, photo_id, photo):                                           
    try:          
        photo = photo.decode("utf-8")
        photo = ast.literal_eval(photo)                                                                                                                           
        ph = mongo_put_data(display_name, photo_id, photo['title'], photo['location'], photo['comment'], photo['tags'])                     
        return 'Modified', 202
    except pymongo.errors.ServerSelectionTimeoutError as sste:                  
        return 'Mongo unavailable', 503      
    except (Photo.DoesNotExist, InvalidId) as e:
        return 'Not Found', 404
       
