from flask import Flask, request, jsonify
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

if __name__ == '__main__':
    app.run(debug=True)
