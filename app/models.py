from flask import current_app
from itsdangerous import URLSafeTimedSerializer as Serializer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, func
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class Book(db.Model):
  __tablename__ = 'books'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(256))
  slug = db.Column(db.String(256), unique=True)
  author = db.Column(db.String(256))
  group = db.Column(db.String(32))
  ratings = db.relationship('Rating', backref='book', lazy='dynamic')

  @hybrid_property
  def average(self):
    ratings = [r.rating for r in self.ratings]
    return round(sum(ratings) / len(ratings), 1)

  @average.expression
  def average(cls):
    return select(func.sum(Rating.rating)) \
        .where(Rating.book_id == cls.id).as_scalar()

  def __repr__(self):
    return '<Book %r by %s>' % (self.title, self.author)

  def ratings_list(self):
    ratings_list = [{'user': r.user.name, 'rating': r.rating} for r in self.ratings]
    ratings_list.sort(key = lambda x: x['user'])
    return ratings_list


class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(256))
  email = db.Column(db.String(64), unique=True, index=True)
  password_hash = db.Column(db.String(128))
  ratings = db.relationship('Rating', backref='user', lazy='dynamic')

  @property
  def password(self):
    raise AttributeError('password is not a readable attribute')

  @password.setter
  def password(self, password):
    if len(password) < 8:
      raise ValueError('Password must be 8 or more characters')
    self.password_hash = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)

  def generate_auth_token(self):
    s = Serializer(current_app.config['SECRET_KEY'])
    return s.dumps({'id': self.id})

  def ratings_list(self):
    ratings_list = [r.as_json() for r in self.ratings]
    ratings_list.sort(key = lambda x: x['Rating'], reverse=True)
    return ratings_list

  def __repr__(self):
    return '<User %r>' % self.name


class Rating(db.Model):
  __tablename__ = 'ratings'
  id = db.Column(db.Integer, primary_key=True)
  book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  rating = db.Column(db.Numeric)

  def as_json(self):
    return {'Title': self.book.title, 'Author': self.book.author, 'Rating': self.rating}

  def __repr__(self):
    if not self.book or not self.user:
      return '<Rating UNINITIALIZED>'

    return '<Rating of %r by %r: %r>' % (self.book.title, self.user.name,
                                         self.rating)
