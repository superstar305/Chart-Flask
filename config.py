import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
  """Base Config Object"""
  
  DEBUG = False
  SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'root'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', '127.0.0.1'),
    os.getenv('DB_NAME', 'test_db')
  )) 

  # This is just here to suppress a warning from SQLAlchemy as it will soon be removed
  # postgresql://postgres:root@localhost:5432/postgres
  SQLALCHEMY_TRACK_MODIFICATIONS = False 