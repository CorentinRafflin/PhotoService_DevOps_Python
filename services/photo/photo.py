from mongoengine import *

class Photo(Document):
    title = StringField(max_length=120, required=False)
    location = StringField(max_length=120, required=False)
    author = StringField(max_length=120, required=True)
    comment = StringField(max_length=120, required=False)
    tags = ListField(max_length=120, required=False)
    photo = FileField()
    meta = {'db_alias': 'default'}

class Photographer(Document):
    interests = ListField(StringField(max_length=30))
    last_name = StringField(max_length=120, required=True)
    display_name = StringField(max_length=120, required=True)
    first_name = StringField(max_length=120, required=True)
    meta = {'db_alias': 'db_photographers'}
