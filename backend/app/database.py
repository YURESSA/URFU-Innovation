from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.paths import DB_PATH

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def ensure_schema():
    with engine.begin() as connection:
        user_columns = connection.exec_driver_sql("PRAGMA table_info(users)").fetchall()
        column_names = {column[1] for column in user_columns}

        if "bitrix_exported" not in column_names:
            connection.exec_driver_sql(
                "ALTER TABLE users ADD COLUMN bitrix_exported INTEGER NOT NULL DEFAULT 0"
            )
