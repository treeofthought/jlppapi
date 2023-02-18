from . import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, func


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
    return select(func.sum(Rating.rating)).where(Rating.book_id==cls.id).as_scalar()

  def rating_row_json(self):
    self.ratings.sort(key=lambda x: x.user.name)
    payload = {
      'Title': self.title,
      'Author': self.author,
      'C': self.average
    }

  def __repr__(self):
    return '<Book %r by %s>' % (self.title, self.author)


class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(256))
  ratings = db.relationship('Rating', backref='user', lazy='dynamic')

  def __repr__(self):
    return '<User %r>' % self.name


class Rating(db.Model):
  __tablename__ = 'ratings'
  id = db.Column(db.Integer, primary_key=True)
  book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  rating = db.Column(db.Numeric)

  def __repr__(self):
    if not self.book or not self.user:
      return '<Rating UNINITIALIZED>'

    return '<Rating of %r by %r: %r>' % (self.book.title, self.user.name,
                                         self.rating)
