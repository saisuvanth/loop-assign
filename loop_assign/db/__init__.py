import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

DATABASE_URI = os.environ.get('DATABASE_URI')
engine = create_engine(DATABASE_URI)  # type: ignore

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
