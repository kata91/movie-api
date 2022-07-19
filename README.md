# movie-api

## Description
This repo contains basic test cases for API testing of following endpoints
  [https://developers.themoviedb.org/3/movies/get-top-rated-movies](url)
  [https://developers.themoviedb.org/3/movies/rate-movie](url)

API Key has been obtained by following the steps listed at the link: [https://developers.themoviedb.org/3/getting-started](url)

## Solution
Solution was developed and tested using Visual Studio Code. Python 3.10 has been used.
`api_main.py` contains OS command that kicks off tests from `tests` folder - in our case it is the file `test_movies.py`. 11 basic examples are included in the solution and the base can be expanded by adding other scenarios. Below are examples of one simple API call for GET method which is expected to fail with unathorized status code as we are trying to retrieve movie details but are passing invalid API key

```{python}
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
```

Next snippet is an example of attemt to post invalid rating value (only multiples of 0.5 are accepted as valid rating) and is therefore recognized as bad request. It is first needed to obtain guest ID which is mandatory for commencing a guest session.
```{python}
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
```

Markers have been added to separate test for GET method and for POST method, which could easen differentiation for potential future CI integration.

As already mentioned, not all scenarios have been added due to time limitation - happy to discuss them on call.

## Running solution in VS Code
Simply by navigating to Tests tab, you can select to run tests one by one, or run all the test in row. Output should be as below:

![image](https://user-images.githubusercontent.com/105950708/179721481-feef64a0-14d3-4e1a-8aea-320171b87a51.png)


It can be also run from Terminal, by calling the following command (also added in api_main.py which is refernced in Dockerfile)

`pytest -sv --html=report.html --disable-pytest-warnings`

It should produce output similar to one below:

![image](https://user-images.githubusercontent.com/105950708/179721319-2101ccd6-b75b-4b9d-8ece-28e4841aca4d.png)


## Running solution in Docker

Presuming you have Docker for Desktop configured on your machine, you can proceed with the steps. If not, please visit [https://docs.docker.com/desktop/install/mac-install/](url); section contains installation executables and steps for different OS types.
After setting up Docker Desktop in your local environment, in VS Code (or other editor of choice), select to add Docker image by navigating to the Command Palette (Ctrl+Shift+P) and typing Add Docker Files to Workspace. Dockerfile will be generated with project-related parameters and additional commands that need to be run from terminal as a part of image setup and running tests.

Open VS Code terminal (or any other of your choice), making sure you are positioned in the appropriate project folder and run the following commands:

To create new Docker image use the following command

`docker build --tag docker-api-tests .`

This will create a docker image `docker-api-tests` on which our tests will run
After that step is finished, use following command to start running the tests

`docker run docker-api-tests`

Finally, to copy generated report from Docker container to a local folder use command

`docker cp <CONTAINER_NAME>:/app/report.html report.html`

<CONTAINER_NAME> is referring to the name of the image (eg. laughing_darwin) and app/report.html is the location where report is saved. Report should be opened in any browser and contains list of executed tests, along with the outcome (passed/failed). Example of one of such files can be found in this repo. Needs to be downloaded locally and opened from browser in order to load in correct format. Screenshot of an example report below:
![image](https://user-images.githubusercontent.com/105950708/179739908-9cd2f325-85fa-4929-95e7-b322f5f5cdd6.png)

