from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import MetaData, create_engine
from config import DB_LOGIN, DB_PASSWORD, DB_SERVER, DB_NAME

app = Flask(__name__)
db_url = 'mysql://{}:{}@{}/{}'.format(DB_LOGIN, DB_PASSWORD, DB_SERVER, DB_NAME)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
conn = create_engine(db_url)
META_DATA = MetaData(bind=conn)
META_DATA.reflect()

#remove laterj
@app.route('/')
def testdb():
  try:
    db.session.query(text('1')).from_statement(text('SELECT 1')).all()
    return '<h1>It works.</h1>'
  except Exception as e:
    return e
#---

class User(db.Model):
  __table__ = META_DATA.tables['User']

class Security_Question(db.Model):
  __table__ = META_DATA.tables['SecurityQuestion']

class Security_User(db.Model):
  __table__= META_DATA.tables['SecurityQuestion_User']


@app.route('/user/verify/login', methods=['POST'])
def verify_login():
  
  data = request.get_json()
  if '@' in data['login']:
    user = User.query.filter_by(email=data['login'], password=data['password']).first()
  else:
    user = User.query.filter_by(nickname=data['login'], password=data['password']).first()
  if not user:
    return jsonify({'message': 'User not found'})
  print(user)
  return jsonify({'user' : '200 OK'})
 
#remove later
@app.route('/user', methods=['GET'])
def get_all_users():
  users = User.query.all()
  output = []

  for user in users:
    user_data = {}
    user_data['nickname'] = user.nickname
    output.append(user_data)

  return jsonify({'users': output})

@app.route('/user', methods=['POST'])
def create_user():
  data = request.get_json()
  new_user = User(nickname=data['nickname'], password=['password'], email=data['email'])
  db.session.add(new_user)
  db.session.commit()

  return jsonify({'message': 'New user created!'})
#---

if __name__ == '__main__':
    app.run(debug=True)
