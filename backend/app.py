from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(80), nullable = False)
    lastName = db.Column(db.String(80), nullable = False)
    username = db.Column(db.String(80), nullable = False)
    password = db.Column(db.String(80), nullable = False)
    
    def __repr__(self):
        return '<User %r>' % self.username
    
@app.route('/home', methods=['GET', 'POST'])
def handleGetAndPost():
    if request.method == 'GET':
        return 'get request was received'
    
    if request.method == 'POST':
        return 'post request was received'
    
    
if __name__ == '__main__':
    app.run(debug=True)