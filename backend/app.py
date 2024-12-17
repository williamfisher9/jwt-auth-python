from flask import Flask, request, jsonify, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from sqlalchemy.dialects.sqlite import JSON

app = Flask(__name__)

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

bcrypt = Bcrypt(app)

# JWT configurations
# sets the Flask application's secret key which is used to securely sign session cookies and other security-related needs.
app.config['SECRET_KEY'] = 'your_strong_secret_key'
# sets the secret key used to encode and decode JWTs in for Flask-JWT operations.
app.config["JWT_SECRET_KEY"] = 'your_jwt_secret_key'
# specifies where the application should look for the JWT.
app.config['JWT_TOKEN_LOCATION'] = ['headers']

jwt = JWTManager(app)

# the venue is the URL we are protecting, and the guard 
# protecting the venue is a @jwt_required decorator.
# The @jwt_required decorator is used to protect specific 
# routes that require authentication.
# This decorator will confirm that there's a JWT access 
# token in the request headers before allowing access 
# to the page:


class ErrorResponse():
    def __init__(self, message, status):
        self.message = message
        self.status = status
    
    def to_dict(self):
        return {
            "message": self.message,
            "status": self.status
        }


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    #is_Active = db.Column(db.Boolean, default=True)
    
    
    def __repr__(self):
        return f'<user {self.username}>'
    
    def to_dict(self):
        return {
            "id": self.id, 
            "first_name": self.first_name, 
            "last_name": self.last_name, 
            "username": self.username, 
            "password": self.password
            }



@app.route("/api/v1/users/get_name", methods=["GET"])
@jwt_required()
def get_name():
    print("----------------------------------------------------------")
    user_id = get_jwt_identity()
    print(user_id)
    user = User.query.filter_by(username=user_id).first()
    
    # Check if user exists
    if user:
        return jsonify({'message': 'User found', 'name': user.username})
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/api/v1/users/register', methods=['POST'])
def handle_register_request():
    """
    if request.method == 'GET':
        users = UserModel.query.all()
        print(type(users))
        return jsonify([ob.to_dict() for ob in users])
    """
    if request.method == 'POST':
        user = User(username = request.json['username'], 
                         first_name = request.json['first_name'], 
                         last_name = request.json['last_name'], 
                         password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8'))
        
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as exc:
            error = ErrorResponse(repr(exc), 409)
            #logger.info(repr(exc))
            return jsonify(error.to_dict()), 409
        
        print(user)
        return jsonify(user.to_dict()), 201
    
@app.route('/api/v1/users/login', methods=['POST'])
def handle_login_request():
    try:
        username = request.get_json()['username']
        password = request.get_json()['password']
        
        if not username or not password:
            return ErrorResponse('username/password is null', 403).to_dict()
        
        users = User.query.all()
        user = None
        for user in users:
            if user.username == username:
                user = user
                break
        
        if not user:
            return ErrorResponse('user was not found', 403).to_dict()
        
        if not bcrypt.check_password_hash(user.password, password):
            return ErrorResponse('invalid password', 403).to_dict()
        else:
            access_token = create_access_token(identity=user.username)
            return jsonify({'message': 'Login Success', 'access_token': access_token})
        
    except KeyError as exc:
        return ErrorResponse(repr(exc), 403).to_dict()


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)