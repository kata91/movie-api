import pytest
import requests as r
import json

# ----- Define test data ------

valid_key = '861a6b23efb6fb93bc66300e7ab56c54'
invalid_key = '861a6b23efb6fb93bc66300e7ab56c54asdf'
base_url = 'https://api.themoviedb.org/3/movie/76341?api_key='
base_url_topRated = 'https://api.themoviedb.org/3/movie/top_rated?api_key='
base_url_rating = 'https://api.themoviedb.org/3/movie/507086/rating?api_key='
base_url_guestSession = 'https://api.themoviedb.org/3/authentication/guest_session/new?api_key='

tokenID = ''
guestID = ''

valid_rating= {'value': 9.5}
invalid_rating= {'value': 9.2}

valid_movie_ID = '507086'
invalid_movie_ID = '111111111'

# ------------------
# Class to implement helper functions
class Helpers(object):
    def get_token_id(self):
        response = r.get("https://api.themoviedb.org/3/authentication/token/new?api_key=" + valid_key)
        with open('test\JsonRespContent\RequestToken.json', 'wb') as resp:
            resp.write(response.content)
        with open('test\JsonRespContent\RequestToken.json', 'r') as readJson:
            loadJson = json.load(readJson)
            tokenID = loadJson["request_token"]
            print ("Token is:" + tokenID)    
        auth = r.get("https://www.themoviedb.org/authenticate/" + tokenID)
    
                
# Class that contains our testcases
class TestMovie(object):

    # ----------- Test GET method ------------
    @pytest.mark.GET_Method
    # Get movie with the valid key
    def test_get_movie_status_code_valid_key(self):
        response = r.get(base_url + valid_key)
        assert response.status_code == 200
   
    @pytest.mark.GET_Method
    # Get movie with an invalid key
    def test_get_movie_status_code_invalid_key(self):
        response = r.get(base_url  + invalid_key)
        assert response.status_code == 401
   
    @pytest.mark.GET_Method
    # Try to get non-existing movie with valid key
    def test_get_movie_status_code_invalid_key(self):
        response = r.get(base_url  + invalid_key)
        assert response.status_code == 401

    @pytest.mark.GET_Method
    # Get top rated movies with valid key 
    def test_get_top_rated_status_code_valid_key(self):
        response = r.get(base_url_topRated + valid_key + "&language=en-US&page=1")
        with open('test\JsonRespContent\TopRatedValidKey.json', 'w') as resp:
            json.dump(response.json(), resp,  indent=4)
        assert response.status_code == 200

    @pytest.mark.GET_Method
    # Try to get top rated movies with invalid key 
    def test_get_top_rated_status_code_invalid_key(self):
        response = r.get(base_url_topRated + invalid_key + "&language=en-US&page=1")
        with open('test\JsonRespContent\TopRatedInvalidKey.json', 'w') as resp:
            json.dump(response.json(), resp,  indent=4)
        assert response.status_code == 401
        
    # ------------ Test POST method--------------------
    @pytest.mark.POST_Method
    # Post rating with valid key unauthorized
    def test_post_rating_valid_key_unauthorized(self):
        response = r.post(base_url_rating + valid_key)
        with open('test\JsonRespContent\PostRatingUnathorized.json', 'w') as resp:
            json.dump(response.json(), resp,  indent=4)
        assert response.status_code == 401

    @pytest.mark.POST_Method
    # Post rating with valid key authorized
    def test_post_rating_valid_key_authorized(self):    
        guest_session = r.get(base_url_guestSession + valid_key)
        with open('test\JsonRespContent\StartGuestSession.json', 'w') as resp:
            json.dump(guest_session.json(), resp,  indent=4)
            resp.close()
        with open('test\JsonRespContent\StartGuestSession.json', 'r') as readJson:
            loadJson = json.load(readJson)
            success = loadJson["success"]
            guest_id = loadJson["guest_session_id"]
            if str(success) == "True":
                response = r.post("https://api.themoviedb.org/3/movie/" + valid_movie_ID + "/rating?api_key=" + valid_key + "&guest_session_id=" + guest_id, valid_rating)
                assert response.status_code == 201
            else:
                print("Could not retrieve guest session!")
    
    @pytest.mark.POST_Method
    # Try to post invalid rating value with valid key authorized
    def test_post_invalid_rating_valid_key_authorized(self):    
        guest_session = r.get(base_url_guestSession + valid_key)
        with open('test\JsonRespContent\StartGuestSession.json', 'w') as resp:
            json.dump(guest_session.json(), resp,  indent=4)
            resp.close()
        with open('test\JsonRespContent\StartGuestSession.json', 'r') as readJson:
            loadJson = json.load(readJson)
            success = loadJson["success"]
            guest_id = loadJson["guest_session_id"]
        readJson.close()
        if str(success) == "True":
            response = r.post("https://api.themoviedb.org/3/movie/" + valid_movie_ID + "/rating?api_key=" + valid_key + "&guest_session_id=" + guest_id, invalid_rating)
            assert response.status_code == 400 

    @pytest.mark.POST_Method
    # Try to post rating with invalid key
    def test_post_rating_invalid_key(self):    
        guest_session = r.get(base_url_guestSession + valid_key)
        with open('test\JsonRespContent\StartGuestSession.json', 'w') as resp:
            json.dump(guest_session.json(), resp,  indent=4)
            resp.close()
        with open('test\JsonRespContent\StartGuestSession.json', 'r') as readJson:
            loadJson = json.load(readJson)
            success = loadJson["success"]
            guest_id = loadJson["guest_session_id"]
            readJson.close()
        if str(success) == "True":
            response = r.post("https://api.themoviedb.org/3/movie/" + valid_movie_ID + "/rating?api_key=" + invalid_key + "&guest_session_id=" + guest_id, invalid_rating)
            assert response.status_code == 401

    @pytest.mark.POST_Method
    # Try to get guest session with invalid key
    def test_post_valid_rating_invalid_guest_session(self):    
        guest_session = r.get(base_url_guestSession + invalid_key)
        with open('test\JsonRespContent\StartGuestSession.json', 'w') as resp:
            json.dump(guest_session.json(), resp,  indent=4)
            resp.close()
        assert guest_session.status_code == 401 

    @pytest.mark.POST_Method
    # Try to post valid rating to the invalid movie ID
    def test_post_valid_rating_invalid_movie(self):    
        guest_session = r.get(base_url_guestSession + valid_key)
        with open('test\JsonRespContent\StartGuestSession.json', 'w') as resp:
            json.dump(guest_session.json(), resp,  indent=4)
            resp.close()
        with open('test\JsonRespContent\StartGuestSession.json', 'r') as readJson:
            loadJson = json.load(readJson)
            success = loadJson["success"]
            guest_id = loadJson["guest_session_id"]
        readJson.close()
        if str(success) == "True":
            response = r.post("https://api.themoviedb.org/3/movie/" + invalid_movie_ID + "/rating?api_key=" + valid_key + "&guest_session_id=" + guest_id, valid_rating)
            assert response.status_code == 404   
