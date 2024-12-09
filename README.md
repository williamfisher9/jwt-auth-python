# JWT authentication using Flask
An application to secure a Flask REST API using JWT authentication

## Running the App:
1. Clone the repository
2. Create a virtual environment `py -m venv .venv`
3. Run the virtual environment profile `source .venv/Scripts/activate`
4. Install the dependencies `pip install -r requirements.txt`
5. Create the database and models:
    ```
        $ python
        >>> from app import app, db
        >>> with app.app_context():
        >>>     db.create_all()
    ```
6. Start the app `py app.py` or `flask --app app run --debug`

## General Info:
```
# create a virtual environment profile int he backend folder
py -m venv .venv
```

```
# run the virtual environment profile
source .venv/Scripts/activate
```

```
# install dependencies
pip install Flask PyJWT Flask_SQLAlChemy
```

```
# show installed packages
pip freeze

# save installed packages in the requirements folder
pip freeze > requirements.txt

# to install dependencies in the requirements.txt
pip install -r requirements.txt
```

```
# run the below commands to create sqlite3 database and model tables
$ python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
```

```
# start the app by running the commands int he project folder
source .venv/Scripts/activate
py app.py
```

```
# Flask app can be started by running the below command without the need for app.run:
flask --app app run --debug

# or by adding app.run and then:
py app.py
```

```
# Hash passwords using bcrypt
pip install Flask-Bcrypt
```