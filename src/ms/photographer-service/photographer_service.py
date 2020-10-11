#!/usr/bin/env python3

import logging
import json

import connexion
from connexion import NoContent
from photographer import Photographer
from mongoengine import *
from bson.objectid import ObjectId
from bson import json_util
from bson.errors import InvalidId
import pymongo
from flask import jsonify
import json
import flask

from photographer_mongo_wrapper import *

# See:
# https://devops.com/pymongo-pointers-make-robust-highly-available-mongo-queries
# for Robust Mongo Queries

def get_photographers(offset, limit):
    try:
        ids = mongo_get_photographers(offset, limit)
    except pymongo.errors.ServerSelectionTimeoutError as sste:
        return 503
    return json.loads(json.dumps(ids)) # is it necessary ?

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

def post_photographers(photographer):                                           
    try:                                                                        
        if mongo_check(photographer['display_name']) > 0:                       
            return 'Conflict', 409                                              
        else:                                                                   
            ph = mongo_add (photographer['display_name'],                       
                            photographer['first_name'],                         
                            photographer['last_name'],                          
                            photographer['interests'])                          
            return 'Created', 201, {'location': '/photographer/' + str(ph.display_name)} 
    except (pymongo.errors.AutoReconnect,
            pymongo.errors.ServerSelectionTimeoutError,
            pymongo.errors.NetworkTimeout) as e:
        return 'Mongo unavailable', 503                                                 

def delete_photographer(display_name):
    try:
        ph = mongo_delete_photographer_by_name(display_name)
        if ph:
            return 'NoContent', 204
        else:
            return 'Not Found', 404
    except (pymongo.errors.AutoReconnect,
            pymongo.errors.ServerSelectionTimeoutError,
            pymongo.errors.NetworkTimeout) as e:
        return 'Mongo unavailable', 503                                                 



