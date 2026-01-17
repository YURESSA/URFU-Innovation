from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.paths import DB_PATH

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
