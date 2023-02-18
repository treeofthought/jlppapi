import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_DATABASE_URI = "postgresql://jlppbc-admin:@localhost:5432/jlppapi"
  SQLALCHEMY_ECHO = True

  @staticmethod
  def init_app(app):
    pass


config = {
    'default': Config
}
