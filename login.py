from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import MetaData, create_engine
from config import DB_LOGIN, DB_PASSWORD, DB_SERVER, DB_NAME
from cryptography.fernet import Fernet
import argparse


#gets runtime arguments
parser = argparse.ArgumentParser()
parser.add_argument("-K", "--key", help="encryption key")
args = parser.parse_args()

#unciphers text (credentials) by using key from runtime arguments and returns them as plain text
def decrypt_credentials(text):
  #check if key was given during runtime
  if not args.key:
    return "No key"
  key = args.key
  cipher_suite = Fernet(key)
  unciphered = cipher_suite.decrypt(text)
  plain_text = bytes(unciphered).decode("utf-8")
  return plain_text

#decrypts sql credentials
db_login = decrypt_credentials(DB_LOGIN)
db_pass = decrypt_credentials(DB_PASSWORD)
db_server = decrypt_credentials(DB_SERVER)
db_name = decrypt_credentials(DB_NAME)
db_url = 'mysql://{}:{}@{}/{}'.format(db_login, db_pass, db_server, db_name)

#flask configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
conn = create_engine(db_url)
META_DATA = MetaData(bind=conn)
META_DATA.reflect()

class User(db.Model):
  __table__ = META_DATA.tables['User']

#checks if database is alive
@app.route('/')
def testdb():
  try:
    db.session.query(text('1')).from_statement(text('SELECT 1')).all()
    return '<h1>It works.</h1>'
  except Exception as e:
    return e

#verifies if login given matches with any db user
@app.route('/user/verify/login', methods=['POST'])
def verify_login():
  try:
    data = request.get_json()
    #check if user login was given as his username or his email
    if '@' in data['login']:
      user = User.query.filter_by(email=data['login'], password=data['password']).first()
    else:
      user = User.query.filter_by(nickname=data['login'], password=data['password']).first()
    if not user:
      return jsonify({'message': 'User not found'})
    print(user)
    return jsonify({'user' : '200 OK'})
  except Exception as e:
    return e

if __name__ == '__main__':
    app.run(debug=True)
