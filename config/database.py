
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

DATABASE_URL: str  = os.getenv("DATABASE_URL") # type: ignore


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

meta = MetaData()

