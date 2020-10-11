#!/usr/bin/env python3

import logging
import json

import connexion
from connexion import NoContent
from photo import Photo
from mongoengine import *
from bson.objectid import ObjectId
from bson import json_util
from bson.errors import InvalidId
import pymongo
from flask import jsonify
import json
import flask
import requests

from photo_const import REQUEST_TIMEOUT

from photo_mongo_wrapper import *

# See:
# https://devops.com/pymongo-pointers-make-robust-highly-available-mongo-queries
# for Robust Mongo Queries

photo_all_attributes = ['title', 'comment', 'location', 'tags']

def upload_photo(display_name, upfile):  
    try:
        filename = upfile.filename
        photographer = requests.get('http://photo-service:8090/photographer/' + display_name,
                                    timeout=REQUEST_TIMEOUT)
        if photographer.status_code == requests.codes.ok:
            id = mongo_allocate_photo_id(display_name)
            if mongo_save_photo(upfile, display_name, id):
                return 'Created', 201, {'location': '/photo/' + display_name + "/" + str(id)}
            else:
                return 'Mongo unavailable', 503
        elif photographer.status_code == requests.codes.unavailable:
            return 'Photographer Service Unavailable', 503
        elif photographer.status_code == requests.codes.not_found:
            return 'Not Found', 404
    except (pymongo.errors.AutoReconnect,
            pymongo.errors.ServerSelectionTimeoutError,
            pymongo.errors.NetworkTimeout) as e:
        return 'Mongo unavailable', 503                                                 

def get_photo(display_name, photo_id):  
    try:
        ph = mongo_get_photo_by_name_and_id(display_name, photo_id)
        return ph.image_file, 200, {'Content-Type': 'application/octet-stream'}
    except (pymongo.errors.AutoReconnect,
            pymongo.errors.ServerSelectionTimeoutError,
            pymongo.errors.NetworkTimeout) as e:
        return 'Mongo unavailable', 503                                                 
    except (Photo.DoesNotExist) as e:
        return 'Not Found', 404
    except (Photo.MultipleObjectsReturned) as e:
        return 'Internal Error', 500

def delete_photo(display_name, photo_id):
    try:
        ph = mongo_delete_photo_by_name_and_id(display_name, photo_id)
        if ph:
            return 'NoContent', 204
        else:
            return 'Not Found', 404
    except (pymongo.errors.AutoReconnect,
            pymongo.errors.ServerSelectionTimeoutError,
            pymongo.errors.NetworkTimeout) as e:
        return 'Mongo unavailable', 503                                                 

def get_photo_attributes(display_name, photo_id):  
    try:
        ph = mongo_get_photo_by_name_and_id(display_name, photo_id)
        ph._data.pop('image_file')
        ph._data.pop('photo_id')
        ph._data.pop('id')
        ph._data.pop('display_name')
        if not ph._data['comment']:
            ph._data.pop('comment')
        if not ph._data['title']:
            ph._data.pop('title')
        if not ph._data['tags']:
            ph._data.pop('tags')
        if not ph._data['location']:
            ph._data.pop('location')
        return json.loads(json.dumps(ph._data, indent=4, default=json_util.default))
    except (pymongo.errors.AutoReconnect,
            pymongo.errors.ServerSelectionTimeoutError,
            pymongo.errors.NetworkTimeout) as e:
        return 'Mongo unavailable', 503                                                 
    except (Photo.DoesNotExist) as e:
        return 'Not Found', 404
    except (Photo.MultipleObjectsReturned) as e:
        return 'Internal Error', 500
    
# This method must replace or update some of the attributes
# PATCH) of the given photo (update ? example - add a tag
# to the list of tags).

def patch_photo_attributes(display_name, photo_id, photo_attributes):
    pass

# This method must replace all the attributes (a PUT is not a
# PATCH) of the given photo.
# if some attribute is not defined in attributes, the method
# will unset the attribute

def set_photo_attributes(display_name, photo_id, attributes):  
    try:
        mongo_set_photo_attributes(display_name, photo_id, attributes, photo_all_attributes)
    except (pymongo.errors.AutoReconnect,
            pymongo.errors.ServerSelectionTimeoutError,
            pymongo.errors.NetworkTimeout) as e:
        return 'Mongo unavailable', 503                                                 
    except (Photo.DoesNotExist) as e:
        return 'Not Found', 404
    except (Photo.MultipleObjectsReturned) as e:
        return 'Internal Error', 500

def get_photos(display_name, offset, limit):  
    try:
        photographer = requests.get('http://photo-service:8090/photographer/' + display_name,
                                    timeout=REQUEST_TIMEOUT)
        if photographer.status_code == requests.codes.ok:
            try:
                photos = mongo_get_photos_by_name(display_name, offset, limit)
                if not photos:
                    return 'No Content', 204
                else:
                    return ["/photo/" + str(ph.photo_id) for ph in photos]
            except (pymongo.errors.AutoReconnect,
                    pymongo.errors.ServerSelectionTimeoutError,
                    pymongo.errors.NetworkTimeout) as e:
                return 'Mongo unavailable', 503                                                 
        elif photographer.status_code == requests.codes.unavailable:
            return 'Photographer Service Unavailable', 503
        elif photographer.status_code == requests.codes.not_found:
            return 'Not Found', 404
        else:
            # Calling raise_for_status() will raise an exception in case of error code
            photographer.raise_for_status() 
    except requests.exceptions.RequestException as e:
        return 'Photographer Service Unavailable', 503
