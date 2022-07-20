import pytest
import requests as r
import json

# ----- Define test data ------

valid_key = '861a6b23efb6fb93bc66300e7ab56c54'
invalid_key = '861a6b23efb6fb93bc66300e7ab56c54asdf'
base_url = 'https://api.themoviedb.org/3/movie/76341?api_key='
base_url_invalidMovie = 'https://api.themoviedb.org/3/movie/763412764?api_key='
base_url_topRated = 'https://api.themoviedb.org/3/movie/top_rated?api_key='
base_url_rating_valid = 'https://api.themoviedb.org/3/movie/507086/rating?api_key='
base_url_rating_invalid = 'https://api.themoviedb.org/3/movie/5070861468/rating?api_key='
base_url_guestSession = 'https://api.themoviedb.org/3/authentication/guest_session/new?api_key='
jsonReport_location = 'test\JsonRespContent'

tokenID = ''
guestID = ''

valid_rating= {'value': 9.5}
invalid_rating= {'value': 9.2}

valid_movie_ID = '507086'
invalid_movie_ID = '111111111'

#------------------
# Class to implement helper functions - this is never used
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
        # API response for get method; passing valid API key as argument
        response = r.get(base_url + valid_key)
        # Saves json response content in desired location
        with open(jsonReport_location + '\GetMovieValidKey.json', 'w') as resp:
            json.dump(response.json(), resp,  indent=4)
        # Asserts response code for successful get action
        assert response.status_code == 200
   
    @pytest.mark.GET_Method
    # Get movie with an invalid key
    def test_get_movie_status_code_invalid_key(self):
        # API response for get method; passing invalid API key as argument
        response = r.get(base_url  + invalid_key)
        # Saves json response content in desired location
        with open(jsonReport_location + '\GetMovieInvalidKey.json', 'w') as resp:
            json.dump(response.json(), resp,  indent=4)
        # Asserts response code for unathorized access
        assert response.status_code == 401
   
    @pytest.mark.GET_Method
    # Try to get non-existing movie with valid key
    def test_get_invalid_movie_status_code_valid_key(self):
        # Passing invalid movie id and valid key
        response = r.get(base_url_invalidMovie  + valid_key)
        with open(jsonReport_location + '\GetInvalidMovieValidKey.json', 'w') as resp:
            json.dump(response.json(), resp,  indent=4)
        assert response.status_code == 404

    @pytest.mark.GET_Method
    # Get top rated movies with valid key 
    def test_get_top_rated_status_code_valid_key(self):
        response = r.get(base_url_topRated + valid_key)
        # Saves json response content in desired location
        with open(jsonReport_location + '\GetTopRatedValidKey.json', 'w') as resp:
            json.dump(response.json(), resp,  indent=4)
        # Asserts success status response
        assert response.status_code == 200

    @pytest.mark.GET_Method
    # Try to get top rated movies with invalid key 
    def test_get_top_rated_status_code_invalid_key(self):
        # Passing url to get top rated movie but uses invalid API key
        response = r.get(base_url_topRated + invalid_key)
        # Saves json response content in desired location
        with open(jsonReport_location + '\GetTopRatedInvalidKey.json', 'w') as resp:
            json.dump(response.json(), resp,  indent=4)
        # Asserts unathorized status response
        assert response.status_code == 401


    # ------------ Test POST method--------------------
    @pytest.mark.POST_Method
    # Post rating with valid key unauthorized
    def test_post_rating_valid_key_unauthorized(self):
        response = r.post(base_url_rating_valid + valid_key)
        with open(jsonReport_location + '\PostRatingUnathorized.json', 'w') as resp:
            json.dump(response.json(), resp,  indent=4)
        # Asserts unathorized status code - no session id passed
        assert response.status_code == 401

    @pytest.mark.POST_Method
    # Post rating with valid key authorized
    def test_post_rating_valid_key_authorized(self):    
        guest_session = r.get(base_url_guestSession + valid_key)
        with open(jsonReport_location + '\StartGuestSession.json', 'w') as resp:
            # Saves json response content in desired location
            json.dump(guest_session.json(), resp,  indent=4)
            resp.close()
        # Reads saved response content in order to obtain success state and guest session id
        with open(jsonReport_location + '\StartGuestSession.json', 'r') as readJson:
            loadJson = json.load(readJson)
            success = loadJson["success"]
            guest_id = loadJson["guest_session_id"]
            # If guest session is successfully started - has "success: true" in json response file, try to post rating 
            if str(success) == "True":
                response = r.post(base_url_rating_valid + valid_key + "&guest_session_id=" + guest_id, valid_rating)
                with open(jsonReport_location + '\PostRatingAuthorized.json', 'w') as resp:
                    # Saves json response content in desired location
                    json.dump(response.json(), resp,  indent=4)
                # Asserts that rating is successfully posted
                assert response.status_code == 201
            else:
                print("Could not retrieve guest session!")

    @pytest.mark.POST_Method
    # Try to post invalid rating value with valid key authorized
    def test_post_invalid_rating_valid_key_authorized(self):    
        guest_session = r.get(base_url_guestSession + valid_key)
        # Saves json response content in desired location
        with open(jsonReport_location + '\StartGuestSession.json', 'w') as resp:
            json.dump(guest_session.json(), resp,  indent=4)
            resp.close()
        # Reads saved response content in order to obtain success state and guest session id
        with open(jsonReport_location + '\StartGuestSession.json', 'r') as readJson:
            loadJson = json.load(readJson)
            success = loadJson["success"]
            guest_id = loadJson["guest_session_id"]
        readJson.close()
        # If guest session is successfully started - has "success: true" in json response file, try to post rating using invalid rating value
        if str(success) == "True":
            response = r.post(base_url_rating_valid + valid_key + "&guest_session_id=" + guest_id, invalid_rating)
            # Request syntax not valid - rating in wrong format
            assert response.status_code == 400 

    @pytest.mark.POST_Method
    # Try to post rating with invalid key
    def test_post_rating_invalid_key(self):    
        guest_session = r.get(base_url_guestSession + valid_key)
        # Saves json response content in desired location
        with open(jsonReport_location + '\StartGuestSession.json', 'w') as resp:
            json.dump(guest_session.json(), resp,  indent=4)
            resp.close()
        # Reads saved response content in order to obtain success state and guest session id
        with open('test\JsonRespContent\StartGuestSession.json', 'r') as readJson:
            loadJson = json.load(readJson)
            success = loadJson["success"]
            guest_id = loadJson["guest_session_id"]
            readJson.close()
        # If guest session is successfully started - has "success: true" in json response file, try to post rating using invalid api key
        if str(success) == "True":
            response = r.post(base_url_rating_valid + invalid_key + "&guest_session_id=" + guest_id, valid_rating)
            # Asserts unathorized status response
            assert response.status_code == 401

    @pytest.mark.POST_Method
    # Try to get guest session with invalid key
    def test_post_valid_rating_invalid_guest_session(self):    
        guest_session = r.get(base_url_guestSession + invalid_key)
        # Saves json response content in desired location
        with open(jsonReport_location + '\StartGuestSession.json', 'w') as resp:
            json.dump(guest_session.json(), resp,  indent=4)
            resp.close()
        # Asserts unathorized status response
        assert guest_session.status_code == 401 

    @pytest.mark.POST_Method
    # Try to post valid rating to the invalid movie ID during a valid guest session 
    def test_post_valid_rating_invalid_movie(self):    
        guest_session = r.get(base_url_guestSession + valid_key)
        # Saves json response content in desired location
        with open(jsonReport_location + '\StartGuestSession.json', 'w') as resp:
            json.dump(guest_session.json(), resp,  indent=4)
            resp.close()
        # Reads saved response content in order to obtain success state and guest session id
        with open(jsonReport_location +'\StartGuestSession.json', 'r') as readJson:
            loadJson = json.load(readJson)
            success = loadJson["success"]
            guest_id = loadJson["guest_session_id"]
        readJson.close()
        # If guest session is successfully started - has success: true in json response file, try to post rating for invalid movie id
        if str(success) == "True":
            # Posts 
            response = r.post(base_url_rating_invalid + valid_key + "&guest_session_id=" + guest_id, valid_rating)
            # Resource not found, asserts not found status
            assert response.status_code == 404   
