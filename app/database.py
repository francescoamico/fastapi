#we're going to use an ORM(Object-Relational Mapping) instead of using raw SQL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
#using SQL directly
import psycopg2 
from psycopg2.extras import RealDictCursor
import time

while True:
    try:
        conn = psycopg2.connect(host=f"{settings.database_hostname}", database=f"{settings.database_name}", user=f"{settings.database_username}",
                                password=f"{settings.database_password}", port=f"{settings.database_port}", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        break
    except Exception as error:
        print("Connecting to database failed:", error)
        time.sleep(2)
'''