from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database

url = 'mysql+pymysql://root:12345678@localhost/symbols'
engine = create_engine(url) # connect to server

if not database_exists(url):
    create_database(url)

engine.execute("USE symbols") # select new db

