import os

from flask import g, jsonify
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import text

from app import create_app, db
from app.models import Book, User
from app.seed_db import seed_db


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

auth = HTTPBasicAuth()

def forbidden(message):
  response = jsonify({'error': 'forbidden', 'message': message})
  response.status_code = 403
  return response

@auth.verify_password
def verify_password(email_or_token, password):
  g.token_used = False
  if email_or_token == '':
    return False
  if password == '':
    g.current_user = User.verify_auth_token(email_or_token)
    g.token_used = True
    return g.current_user is not None
  user = User.query.filter_by(email=email_or_token.lower()).first()
  if not user:
    return False
  g.current_user = user
  return user.verify_password(password)

def read(query):
  with open(f'app/queries/{query}.sql', 'r') as f:
    q = f.read()
    return q


@app.route('/')
def index():
  """List all posts"""
  return jsonify('success')


@app.route('/top-five')
def top_five():
  q = read('top-five')
  result = db.session.execute(text(q))
  headers = result.keys()
  rows = result.all()

  return [dict(zip(headers, row)) for row in rows]


@app.route('/bottom-five')
def bottom_five():
  q = read('bottom-five')
  result = db.session.execute(text(q))
  headers = result.keys()
  rows = result.all()

  return [dict(zip(headers, row)) for row in rows]

@app.route('/books/<slug>', methods=['GET'])
def book_detail(slug):
  b = Book.query.filter_by(slug=slug).first()

  return {'title': b.title, 'author': b.author, 'ratings': b.ratings_list()}

@app.route('/ratings')
def ratings():
  q = read('ratings')
  result = db.session.execute(text(q))
  headers = result.keys()
  rows = result.all()

  return [dict(zip(headers, row)) for row in rows]


@app.route('/ratings/<user>', methods=['GET'])
def ratings_user(user):
  u = User.query.filter_by(name=user).first()
  return u.ratings_list()

@app.route('/tokens', methods=['POST'])
@auth.login_required
def get_token():
  if g.token_used:
    return forbidden('Cannot fetch a token with a token')
  return {
    'token': g.current_user.generate_auth_token(),
    'name': g.current_user.name
  }


@app.shell_context_processor
def make_shell_context():
  return dict(db=db, Book=Book)


@app.cli.command()
def test():
  """Run the unit tests."""
  import unittest
  tests = unittest.TestLoader().discover('tests')
  unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def lint():
  """Run the linter"""
  os.system('flake8')


@app.cli.command()
def seed():
  """Populate the database"""
  seed_db()
