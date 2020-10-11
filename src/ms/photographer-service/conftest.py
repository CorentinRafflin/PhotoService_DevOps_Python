import pytest
import connexion
from mongoengine import connect
from photographer import Photographer

flask_app = connexion.FlaskApp(__name__)
flask_app.add_api('photographer_service.yml')

@pytest.fixture(scope="class")
def client():
    with flask_app.app.test_client() as c:
        yield c

@pytest.fixture
def clearPhotographers():
    Photographer.objects.all().delete()

    
@pytest.fixture(scope="class")
def initDB():
    connect("photographers_test", host="172.17.0.2")
    yield
    # add code to destroy the database ?
