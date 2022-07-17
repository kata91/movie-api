from asyncio.windows_events import NULL
from pydoc import Helper
import requests as r
import json

valid_key = '861a6b23efb6fb93bc66300e7ab56c54'
invalid_key = '861a6b23efb6fb93bc66300e7ab56c54asdf'
tokenID = ''
guestID = ''
valid_rating= {'value': 9.5}
invalid_rating= {'value': 9.2}

class Helpers(object):
    def get_token_id(self):
        response = r.get("https://api.themoviedb.org/3/authentication/token/new?api_key=" + valid_key)
        #rc = json.dumps(response.content, indent = 4)
        with open('test\JsonRespContent\RequestToken.json', 'wb') as resp:
            resp.write(response.content)
            #resp.write(rc)
            #json.dump(resp, indent=4)
        with open('test\JsonRespContent\RequestToken.json', 'r') as readJson:
            loadJson = json.load(readJson)
            tokenID = loadJson["request_token"]
            print ("Token is:" + tokenID)    
        auth = r.get("https://www.themoviedb.org/authenticate/" + tokenID)
    
    # def create_guest_session(key):
    #     guest_session = r.get("https://api.themoviedb.org/3/authentication/guest_session/new?api_key=" + key)
    #     with open('test\JsonRespContent\StartGuestSession.json', 'wb') as resp:
    #         resp.write(guest_session.content)
    #         with open('test\JsonRespContent\StartGuestSession.json', 'r') as readJson:
    #             loadJson = json.load(readJson)
    #             success = loadJson["success"]
    #             if success == "true":
    #                 response = r.post("https://api.themoviedb.org/3/movie/507086/rating?api_key=" + valid_key, rating)
                
            

class TestMovie(object):
    #get movie with valid key
    def test_get_movie_status_code_valid_key(self):
        response = r.get("https://api.themoviedb.org/3/movie/76341?api_key=" + valid_key)
        assert response.status_code == 200

    def test_get_movie_status_code_invalid_key(self):
        response = r.get("https://api.themoviedb.org/3/movie/76341?api_key=" + invalid_key)
        assert response.status_code == 401

    def test_get_top_rated_status_code_valid_key(self):
        response = r.get("https://api.themoviedb.org/3/movie/top_rated?api_key=861a6b23efb6fb93bc66300e7ab56c54&language=en-US&page=1")
        with open('test\JsonRespContent\TopRatedValidKey.json', 'wb') as resp:
            resp.write(response.content)
        assert response.status_code == 200

    def test_get_top_rated_status_code_invalid_key(self):
        response = r.get("https://api.themoviedb.org/3/movie/top_rated?api_key=861a6b23efb6fb93bc66300e7ab56c54asdf&language=en-US&page=1")
        with open('test\JsonRespContent\TopRatedInvalidKey.json', 'wb') as resp:
            resp.write(response.content)
        assert response.status_code == 401
        
    #Test POST method
    def test_post_rating_valid_key_unathorized(self):
        response = r.post("https://api.themoviedb.org/3/movie/507086/rating?api_key=861a6b23efb6fb93bc66300e7ab56c54")
        with open('test\JsonRespContent\PostRatingUnathorized.json', 'wb') as resp:
            resp.write(response.content)
        assert response.status_code == 401

    def test_post_rating_valid_key_athorized(self):    
        guest_session = r.get("https://api.themoviedb.org/3/authentication/guest_session/new?api_key=" + valid_key)
        with open('test\JsonRespContent\StartGuestSession.json', 'wb') as resp:
            resp.write(guest_session.content)
        with open('test\JsonRespContent\StartGuestSession.json', 'r') as readJson:
            loadJson = json.load(readJson)
            success = loadJson["success"]
            guest_id = loadJson["guest_session_id"]
            if str(success) == "True":
                response = r.post("https://api.themoviedb.org/3/movie/507086/rating?api_key=" + valid_key + "&guest_session_id=" + guest_id, valid_rating)
                assert response.status_code == 201 
                # pusa za milu
    
    def test_post_invalid_rating_valid_key_athorized(self):    
        guest_session = r.get("https://api.themoviedb.org/3/authentication/guest_session/new?api_key=" + valid_key)
        with open('test\JsonRespContent\StartGuestSession.json', 'wb') as resp:
            resp.write(guest_session.content)
        with open('test\JsonRespContent\StartGuestSession.json', 'r') as readJson:
            loadJson = json.load(readJson)
            success = loadJson["success"]
            guest_id = loadJson["guest_session_id"]
            if str(success) == "True":
                response = r.post("https://api.themoviedb.org/3/movie/507086/rating?api_key=" + valid_key + "&guest_session_id=" + guest_id, invalid_rating)
                assert response.status_code == 400 

    def test_post_rating_invalid_key(self):    
        guest_session = r.get("https://api.themoviedb.org/3/authentication/guest_session/new?api_key=" + valid_key)
        with open('test\JsonRespContent\StartGuestSession.json', 'wb') as resp:
            resp.write(guest_session.content)
        with open('test\JsonRespContent\StartGuestSession.json', 'r') as readJson:
            loadJson = json.load(readJson)
            success = loadJson["success"]
            guest_id = loadJson["guest_session_id"]
            if str(success) == "True":
                response = r.post("https://api.themoviedb.org/3/movie/507086/rating?api_key=" + invalid_key + "&guest_session_id=" + guest_id, invalid_rating)
                assert response.status_code == 401

    def test_post_valid_rating_invalid_guest_session(self):    
        guest_session = r.get("https://api.themoviedb.org/3/authentication/guest_session/new?api_key=" + invalid_key)
        with open('test\JsonRespContent\StartGuestSession.json', 'wb') as resp:
            resp.write(guest_session.content)
        assert guest_session.status_code == 401 

    def test_post_valid_rating_invalid_movie(self):    
        guest_session = r.get("https://api.themoviedb.org/3/authentication/guest_session/new?api_key=" + valid_key)
        with open('test\JsonRespContent\StartGuestSession.json', 'wb') as resp:
            resp.write(guest_session.content)
        with open('test\JsonRespContent\StartGuestSession.json', 'r') as readJson:
            loadJson = json.load(readJson)
            success = loadJson["success"]
            guest_id = loadJson["guest_session_id"]
            if str(success) == "True":
                response = r.post("https://api.themoviedb.org/3/movie/507086924/rating?api_key=" + valid_key + "&guest_session_id=" + guest_id, valid_rating)
                assert response.status_code == 404        
    #def test_post_rating_valid_session()

    #def test_post_rating_invalid_key()

    #def test_post_rating_invalid_session()

    #Helpers.get_token_id()