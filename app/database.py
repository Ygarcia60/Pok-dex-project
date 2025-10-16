from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchesoumy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./pokemon.db"