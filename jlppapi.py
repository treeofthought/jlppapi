import os

from flask import jsonify
from flask_migrate import Migrate
from sqlalchemy import text

from app import create_app, db
from app.models import Book
from app.seed_db import seed_db


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

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


@app.route('/ratings')
def ratings():
  q = read('ratings')
  result = db.session.execute(text(q))
  headers = result.keys()
  rows = result.all()

  return [dict(zip(headers, row)) for row in rows]  

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
