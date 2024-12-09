from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='app_info_log.log', level=logging.INFO)

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(80), nullable = False)
    lastName = db.Column(db.String(80), nullable = False)
    username = db.Column(db.String(80), nullable = False, unique = True)
    password = db.Column(db.String(80), nullable = False)
    
    def __str__(self):
        return f"User details {self.id} {self.firstName} {self.lastName} {self.username}>"
    
    def __repr__(self):
        return f"<UserModel {self.id} {self.firstName} {self.lastName} {self.username}>"
    
    def to_dict(self):
        return {
            "id": self.id, 
            "firstName": self.firstName, 
            "lastName": self.lastName, 
            "username": self.username, 
            "password": self.password
            }
        
class ErrorResponse():
    def __init__(self, message, status):
        self.message = message
        self.status = status
    
    def to_dict(self):
        return {
            "message": self.message,
            "status": self.status
        }
        
    
@app.route('/api/v1/users', methods=['GET', 'POST'])
def handle_get_and_post():
    if request.method == 'GET':
        users = UserModel.query.all()
        print(type(users))
        return jsonify([ob.to_dict() for ob in users])
    
    if request.method == 'POST':
        user = UserModel(username = request.json['username'], 
                         firstName = request.json['firstName'], 
                         lastName = request.json['lastName'], 
                         password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8'))
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as exc:
            print("exception occurred")
            error = ErrorResponse(repr(exc), 401)
            logger.info('Started')
            return jsonify(error.to_dict())
        print(user)
        return jsonify(user.to_dict())
    
@app.route('/api/v1/users/<id>', methods=['DELETE', 'PATCH'])
def handle_delete_and_patch(id):
    if request.method == 'DELETE':
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            return {"error": 'not found'}, 404
        db.session.delete(user)
        db.session.commit()
        
        users = UserModel.query.all()
        return jsonify([ob.to_dict() for ob in users]), 202
    
    if request.method == 'PATCH':
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            return {"error": "not found"}, 404
        
        request_params = request.get_json()
        for attr in request_params:
            print(attr)
            print(request_params[attr])
            setattr(user, attr, request_params[attr])
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 202