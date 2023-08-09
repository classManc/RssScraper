# RssScraper
An application that allows user to  create, delete, get Feeds and Feed items


## required packages

pip3 install redis

pip3 install celery

brew install redis

## Installation

1. Clone the repository
    git clone  https://github.com/<username>/RssScraper.git

2. Create a virtual environment and activate Installation
 python3 -m venv venv
    source venv/bin/activate

3. Install the dependencies
    pip install -r requirements.txt

4. Set up the DB
    python manage.py migrate

5. Start the server
    python manage.py runserver


