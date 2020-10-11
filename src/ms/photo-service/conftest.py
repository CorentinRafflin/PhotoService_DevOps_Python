import pytest
import connexion
from mongoengine import connect
from photo import Photo
from photoId import PhotoId

flask_app = connexion.FlaskApp(__name__)
flask_app.add_api('photo_service.yml')

@pytest.fixture(scope="class")
def client():
    with flask_app.app.test_client() as c:
        yield c

@pytest.fixture
def clearPhotos():
    Photo.objects.all().delete()
    PhotoId.objects.all().delete()
    
@pytest.fixture(scope="class")
def initDB():
    connect("photo_test", host="172.17.0.2", alias="photos")
    connect("photoId_test", host="172.17.0.2", alias="photosIds")
    yield
    # add code to destroy the database ?
