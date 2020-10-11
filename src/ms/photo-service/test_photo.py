import pytest
import connexion
import json
from bson import json_util
import logging

import base64,zlib, shutil
from io import BytesIO

from unittest.mock import Mock, patch
from nose.tools import assert_is_not_none

logging.basicConfig(level=logging.DEBUG)

@pytest.mark.usefixtures("clearPhotos")
@pytest.mark.usefixtures("initDB")
class TestClass(object):

    headers_content = {'Content-Type': 'multipart/form-data'}
    headers_accept  = {'Accept': 'application/json'}

    @staticmethod
    def test_post_once(client):
        with patch('photo_service.requests.get') as mock_get:
            # here, we force the Photographer service to return 200 OK.
            mock_get.return_value.status_code = 200
            image_file=BytesIO(base64.decodebytes(encoded_image))
            files = {'file': image_file}

            response = client.post('/gallery/joe', headers=TestClass.headers_content,
                                   data={'upfile': (image_file, 'test.jpg')})

        assert response.headers['Location']
        assert response.status_code == 201

    @staticmethod
    def test_post_once_with_unknown_photographer(client):
        with patch('photo_service.requests.get') as mock_get:
            # here, we force the Photographer service to return 404 Not Found.
            mock_get.return_value.status_code = 404
            image_file=BytesIO(base64.decodebytes(encoded_image))
            files = {'file': image_file}

            response = client.post('/gallery/joe', headers=TestClass.headers_content,
                                   data={'upfile': (image_file, 'test.jpg')})

        assert response.status_code == 404

    @staticmethod
    def test_post_once_and_get(client):
        print (type(client))
        with patch('photo_service.requests.get') as mock_get:
            # here, we force the Photographer service to return 200 OK.
            mock_get.return_value.status_code = 200
            image_file=BytesIO(base64.decodebytes(encoded_image))
            files = {'file': image_file}

            response1 = client.post('/gallery/joe', headers=TestClass.headers_content,
                                   data={'upfile': (image_file, 'test.jpg')})

        assert response1.status_code == 201
        response2 = client.get('/photo/joe/0')
        assert response2.status_code == 200
        assert base64.encodebytes(response2.data) == encoded_image

    @staticmethod
    def test_post_two_photos_and_get_the_list(client):
        with patch('photo_service.requests.get') as mock_get:
            # here, we force the Photographer service to return 200 OK.
            mock_get.return_value.status_code = 200
            image_file=BytesIO(base64.decodebytes(encoded_image))
            #files = {'file': image_file}

            response1 = client.post('/gallery/joe', headers=TestClass.headers_content,
                                   data={'upfile': (image_file, 'test.jpg')})
            
            image_file=BytesIO(base64.decodebytes(encoded_image))
            response2 = client.post('/gallery/joe', headers=TestClass.headers_content,
                                   data={'upfile': (image_file, 'test.jpg')})

            assert response1.status_code == 201
            assert response2.status_code == 201

            response3 = client.get('/gallery/joe')
            json_response3 = json.loads(response3.get_data(as_text=True))
            assert json_response3 == ["/photo/0", "/photo/1"]

        
encoded_image= b"""\
/9j/wAARCABaAIYDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QA
tRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkK
FhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJ
ipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx
8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcF
BAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygp
KjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJma
oqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9sA
QwAcHBwcHBwwHBwwRDAwMERcRERERFx0XFxcXFx0jHR0dHR0dIyMjIyMjIyMqKioqKioxMTExMTc
3Nzc3Nzc3Nzc/9sAQwEiJCQ4NDhgNDRg5pyAnObm5ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubm
5ubm5ubm5ubm5ubm5ubm5ubm5ubm/90ABAAJ/9oADAMBAAIRAxEAPwDQBp4NQA08GkBODTwagBp4
NAEwNOqMGn0AOzUbAnpUlOAFO4GezEtinrCW5NXSiE5xzS4x0quYVikwKdaeobHtVgorHJFDA44p
XHYqFv71RhhjimsGJJalA7CrsRcecHjrUEhI4FWgh25HFR7FHLcmkmNoqbSaTY1WjTarmFyn/9Cy
DTwaiFOzQBMDTwagBp4NAFgGpAarqalBpATCpBUANSA0hktFMzS5oAWijNBNMCCWNTUexQOamY1C
TTuKwFqhY04mmGmhDDSUppKoD//Rl6UuacUHY0zY3Uc0KSCzHZpwNQnK9RigNTAshqkDVU3U8NSA
uBqlDVTUk1NntSsMm3U8NVfNPBp2Fcn3U0tUWaQmnysVxxNMJpCaTmq5bCuNNMJpSDSbGNIYlFBX
HWkwKYH/0hJFzxkVNlXPzfmKzMOOnNSLKy9axNDQVWXjORTWj7rVYTelTiZW9jTTaE0N5p4p6Df6
ZqcrtHJrZWZm9CNCakAPU0mQOKhkuY4uvJpXSHqX0TIzUwCjrWQNQP3QoqyL2Lblgc+lHMFi6wB6
UxdveqEl+NpCDH1qs1+VHqfejn6Bymu7Animqawf7QlZsYGPpUovJCcj8qHILG5lT1pDLEp2kge1
c7JdzyDAbb9KqjdnkmlcdjqjtbkYxSYHtXNFnYBSeB2pMNS5gsf/04PLPcUY9at4U8A807ZXPc1K
JRfSk2ejYq8Yz160wxL1IIouBWy6HrmpBPIRzQyDuQQPWosc/KfwpiA3EndSKrNIzHk1PuIbaRTs
buq5p3sIpHnvSByOM1e+zKRlePrUTWr/AMJFVzILFUsepNJnIqf7PMOw/Oo2hkX7wp3QhmQOlOGW
7mmbWzjFOwRQAp3A5pNz9DS4J7UgGPvYoAbyaMGlyoo3L6UAf//URQA3HNOaQLyetJMSqfLxVZOS
c81iol3JTOx6cVGZXPGakPCHFVl+8arlQrk23d8x/GgrjnrQvA/GkPUVBYzdxk07cQaa/wB0fWog
etVYkv8AmL0NN82LHBpjcKCPQ1VUdPx/lU2Hcu8NyDSEKR8wqqpO5fpVs96TQyExf3Dj69KjKN/E
v5VZNMzhqdwsVSOeDUZi9OfpWgwB61Ubg8U0ybFcp2pNlWTRVXCx/9k=
"""
