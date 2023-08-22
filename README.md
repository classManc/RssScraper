# RssScraper
An application that allows user to  create, delete, get Feeds and Feed items


## Installation

1. Clone the repository
```bash
   git clone  https://github.com/<username>/RssScraper.git
```

2. Create a virtual environment and activate Installation
```bash
   python3 -m venv venv
    source env/bin/activate
```

3. Install the dependencies
```bash
   pip install -r requirements.txt
```

4. Set up the DB
```bash
    python manage.py migrate
```


5. Start the server
```bash
    python manage.py runserver
```
6)The app should now be running at http://localhost:8000/.

To access the API endpoints, you can use a tool like curl or Postman with the appropriate URLs and headers. Alternatively, you can access the Swagger UI by following the steps below.

To access the Swagger UI, follow these steps:

Make sure the app is running locally or deployed on Fly.io.

Open a web browser and go to the URL http://localhost:8000/swagger/ if running locally, or https://late-wood-9200.fly.dev/swagger/. The Swagger UI should now be displayed, allowing you to interact with the API endpoints using a web interface.

API Endpoints
The following endpoints are available:

Feeds & FeedItems:

GET /feeds/: List all Feeds
POST /feeds/: Create a new feed
GET /feeds/{id}/: Retrieve a specific feed
DELETE /feeds/{id}/: Delete a specific feed
UPDATE /feeds/feeditems/{id}/: get feeditems for a specific feed
GET /feeds/feeditems/: get all feeditems for all feeds belonging to the user


Users:

POST /users/login/: Login a user
POST /users/: Register a new user

Refer to the Swagger UI or the DRF documentation for more information on how to use these endpoints.


