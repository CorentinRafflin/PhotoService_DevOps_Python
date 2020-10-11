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

from flask import jsonify
import json
import flask
import robustify

@robustify.retry_mongo
def mongo_check(display_name):
    count = Photographer.objects(display_name=display_name).count()
    return count

@robustify.retry_mongo
def mongo_add(display_name, first_name, last_name, interests):
    ph = Photographer(display_name = display_name,
                      first_name = first_name,
                      last_name = last_name,
                      interests = interests).save()
    return ph

@robustify.retry_mongo
def mongo_get_photographers(offset, limit):
    qs = Photographer.objects
    return [flask.request.url_root + "photographer/" + str(ph.display_name)
            for ph in qs.order_by('id').skip(offset).limit(limit)]

@robustify.retry_mongo
def mongo_get_photographer_by_id(photographer_id):
    ph = Photographer.objects(id=ObjectId(photographer_id)).get()
    return ph

@robustify.retry_mongo
def mongo_get_photographer_by_name(name):
    ph = Photographer.objects(display_name=name).get()
    return ph

@robustify.retry_mongo
def mongo_delete_photographer_by_name(name):
    ph = Photographer.objects(display_name=name).get().delete()

@robustify.retry_mongo
def mongo_update_photographer_by_name(name, new_first_name, new_last_name, new_interests):
    ph = Photographer.objects(display_name=name).update(first_name=new_first_name, last_name=new_last_name, interests=new_interests)


