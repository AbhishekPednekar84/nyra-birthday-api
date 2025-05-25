import os
import dotenv

from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated


dotenv.load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URI")


engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
