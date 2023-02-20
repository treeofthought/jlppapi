import csv
from .models import Book, Rating, User
from . import db


def load_books():
  books = []
  with open('data/books.csv', newline='') as csvfile:
      spamreader = csv.DictReader(csvfile)
      for row in spamreader:
        if row['group'] == 'JLPPBC':
          books.append(Book(**row))
  db.session.add_all(books)
  db.session.commit()


def load_ratings():
  with open('data/ratings.csv', newline='') as csvfile:
    spamreader = csv.DictReader(csvfile)
    for row in spamreader:
      r = create_rating(**row)
      if r:
        db.session.add(r)
        db.session.commit()


def load_users():
  users = [User(name=letter) for letter in ['C', 'D', 'G', 'J', 'P']]

  db.session.add_all(users)
  db.session.commit()

  s = User(name='S', email='strtmason@gmail.com')
  s.password = 'password'
  db.session.add(s)
  db.session.commit()


def create_rating(title, author, rating, user, **kwargs):
  b = Book.query.filter_by(title=title, author=author).first()
  u = User.query.filter_by(name=user).first()
  if b and u:
    r = Rating(rating=rating)
    r.book = b
    r.user = u
    return r


def seed_db():
  db.drop_all()
  db.create_all()

  load_books()
  load_users()
  load_ratings()
