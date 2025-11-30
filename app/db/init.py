import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from databases import Database

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

metadata = MetaData()
Base = declarative_base(metadata=metadata)

engine = create_engine(DATABASE_URL, future=True)
database = Database(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_models() -> None:
    from app.db import model  # noqa: F401
    Base.metadata.create_all(bind=engine)
