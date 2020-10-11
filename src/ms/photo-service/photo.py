from mongoengine import *

class Photo(Document):
    display_name = StringField(max_length=120, required=True)
    image_file = BinaryField(required=True)
    photo_id = IntField(required=True)
    title = StringField(max_length=100, required=False)
    comment = StringField(max_length=100, required=False)
    location = StringField(max_length=100, required=False)
    tags = ListField(StringField(max_length=30), required=False)

    meta = {'db_alias': 'photos'}
