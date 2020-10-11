#!/usr/bin/env python3

import logging
import json

import connexion
from connexion import NoContent
from bson.objectid import ObjectId
from bson import json_util
from bson.errors import InvalidId
from flask import jsonify
import json
import flask
import requests
from urllib.parse import urlparse

from backend_const import REQUEST_TIMEOUT

photo_service = 'http://photo-service:8080/'
photographer_service = 'http://photographer-service:8090/'

def get_photos(display_name, offset, limit):  
    try:
        photos = requests.get(photo_service + "gallery/" + display_name +
                              '?offset=' + str(offset) +
                              '&limit=' + str(limit),
                              timeout = REQUEST_TIMEOUT)
        if photos.status_code == requests.codes.ok:
            return photos.json()
        elif photos.status_code == requests.codes.not_found:
            return 'Not Found', 404
        elif photos.status_code == requests.codes.unavailable:
            return 'Service Unavailable', 503
        else:
            photos.raise_for_status() 
    except requests.exceptions.RequestException as e:
        return 'Service Unavailable', 503
        
def upload_photo(display_name, upfile):  
    try:
        files = {'upfile': upfile}
        r = requests.post(photo_service + "gallery/" + display_name,
                               files = files,
                               timeout = REQUEST_TIMEOUT)
        if r.status_code == requests.codes.created:
            path = urlparse (r.headers['location']).path
            return 'Created', 201, {'location': path}
        elif r.status_code == requests.codes.not_found:
            return 'Not Found', 404
        elif r.status_code == requests.codes.unavailable:
            return 'Service Unavailable', 503
        else:
            r.raise_for_status() 
    except requests.exceptions.RequestException as e:
        return 'Service Unavailable', 503

def get_photo(display_name, photo_id):  
    try:
        r = requests.get(photo_service + "photo/" + display_name + "/" + str(photo_id),
                         timeout = REQUEST_TIMEOUT)
        if r.status_code == requests.codes.ok:
            return r.content, 200, {'Content-Type': 'application/octet-stream'}
        elif r.status_code == requests.codes.not_found:
            return 'Not Found', 404
        elif r.status_code == requests.codes.unavailable:
            return 'Service Unavailable', 503
        else:
            r.raise_for_status() 
    except requests.exceptions.RequestException as e:
        return 'Service Unavailable', 503

def delete_photo(display_name, photo_id):
    try:
        r = requests.delete(photo_service + "photo/" + display_name + "/" + str(photo_id),
                         timeout = REQUEST_TIMEOUT)

        if r.status_code == requests.codes.no_content:
            return 'NoContent', 204
        elif r.status_code == requests.codes.not_found:
            return 'Not Found', 404
        elif r.status_code == requests.codes.unavailable:
            return 'Service Unavailable', 503
        else:
            r.raise_for_status() 
    except requests.exceptions.RequestException as e:
        return 'Service Unavailable', 503

def get_photo_attributes(display_name, photo_id):  
    try:
        r = requests.get(photo_service + "photo/" + display_name + "/" + str(photo_id) + "/attributes",
                         timeout = REQUEST_TIMEOUT)
        if r.status_code == requests.codes.ok:
            return r.json()
        elif r.status_code == requests.codes.not_found:
            return 'Not Found', 404
        elif r.status_code == requests.codes.unavailable:
            return 'Service Unavailable', 503
        else:
            r.raise_for_status() 
    except requests.exceptions.RequestException as e:
        return 'Service Unavailable', 503
    
def set_photo_attributes(display_name, photo_id, attributes):  
    try:
        r = requests.put(photo_service + "photo/" + display_name + "/" + str(photo_id) + "/attributes",
                         json=attributes,
                         timeout = REQUEST_TIMEOUT)
        if r.status_code == requests.codes.ok:
            return 'OK', 200
        elif r.status_code == requests.codes.not_found:
            return 'Not Found', 404
        elif r.status_code == requests.codes.unavailable:
            return 'Service Unavailable', 503
        else:
            r.raise_for_status() 
    except requests.exceptions.RequestException as e:
        return 'Service Unavailable', 503

def get_photographers(offset, limit):
    try:
        photographers = requests.get(photographer_service + "photographers" +
                                     '?offset=' + str(offset) +
                                     '&limit=' + str(limit),
                                     timeout = REQUEST_TIMEOUT)
        if photographers.status_code == requests.codes.ok:
            return photographers.json()
        elif photographers.status_code == requests.codes.not_found:
            return 'Not Found', 404
        elif photographers.status_code == requests.codes.unavailable:
            return 'Service Unavailable', 503
        else:
            photographers.raise_for_status() 
    except requests.exceptions.RequestException as e:
        return 'Service Unavailable', 503

def get_photographer(display_name):
    try:
        r = requests.get(photographer_service + "photographer/" + display_name,
                         timeout = REQUEST_TIMEOUT)
        if r.status_code == requests.codes.ok:
            return r.json()
        elif r.status_code == requests.codes.not_found:
            return 'Not Found', 404
        elif r.status_code == requests.codes.unavailable:
            return 'Service Unavailable', 503
        else:
            r.raise_for_status() 
    except requests.exceptions.RequestException as e:
        return 'Service Unavailable', 503

def post_photographers(photographer):
    try:
        r = requests.post(photographer_service + "photographers",
                          json=photographer,
                          timeout = REQUEST_TIMEOUT)
        if r.status_code == requests.codes.created:
            path = urlparse (r.headers['location']).path
            return 'Created', 201, {'location': path} 
        elif r.status_code == requests.codes.not_found:
            return 'Not Found', 404
        elif r.status_code == requests.codes.unavailable:
            return 'Service Unavailable', 503
        elif r.status_code == requests.codes.conflict:
            return 'Conflict', 409
        else:
            r.raise_for_status() 
    except requests.exceptions.RequestException as e:
        return 'Service Unavailable', 503

def delete_photographer(display_name):
    try:
        r = requests.delete(photographer_service + "photographer/" + display_name,
                            timeout = REQUEST_TIMEOUT)

        if r.status_code == requests.codes.no_content:
            return 'NoContent', 204
        elif r.status_code == requests.codes.not_found:
            return 'Not Found', 404
        elif r.status_code == requests.codes.unavailable:
            return 'Service Unavailable', 503
        else:
            r.raise_for_status() 
    except requests.exceptions.RequestException as e:
        return 'Service Unavailable', 503
