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


class HerokuConfig(Config):
  heroku_db_url = os.environ.get('DATABASE_URL')
  sqlalchemy_support = heroku_db_url.replace('postgres://', 'postgresql://')
  SQLALCHEMY_DATABASE_URI = sqlalchemy_support

config = {
    'default': Config,
    'heroku': HerokuConfig
}
