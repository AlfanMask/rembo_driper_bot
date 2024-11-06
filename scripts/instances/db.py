# load all env variables
from dotenv import load_dotenv
load_dotenv()
import os

from models.dataengine import Database

# get env variables
host = os.getenv("HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DATABASE")

# create database instance
db = Database(host, user, password, database)