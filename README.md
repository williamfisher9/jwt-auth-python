# JWT authentication using Flask
An application to secure a Flask REST API using JWT authentication
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