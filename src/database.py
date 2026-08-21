from typing import Sequence

from sqlalchemy import engine, create_engine
from sqlalchemy.orm import Session
import os

from src import db_models as model


DB_PATH: str = os.getcwd() + "/db"

# creates ../db if needed
def init_db_dir() -> None:
    try:
        os.mkdir(DB_PATH, mode=0o700)
    except FileExistsError:
        print(f"{DB_PATH} already exists, init skipped")

init_db_dir()


engine = create_engine(f"sqlite:///{DB_PATH}/media-index.sqlite3", echo=False)

model.Base.metadata.create_all(engine)


# takes PIL image obj, str with UUID
# returns store_id (in UUID) as str
def index_new_image(image, id, hash) -> str:
    with Session(engine) as session:
        image_format = image.format
        entry = model.ImageEntry(id=id, filetype=image_format, hash=hash)

        session.add(entry)
        session.commit()

        return id

def index_duplicate_image(image, id, hash, original) -> str:
    with Session(engine) as session:
        image_format = image.format
        entry = model.ImageEntry(id=id, filetype=image_format, hash=hash, duplicate_of=original)

        session.add(entry)
        session.commit()

        return id


def update_duplicate(id, duplicate_of: str | None) -> None:
    with Session(engine) as session:
        entry = session.get(model.ImageEntry, id)
        entry.duplicate_of = duplicate_of
        session.commit()


# takes media_id and queries for file format
def query_first(stmt) -> str | None:
    with Session(engine) as session:
        result = session.scalars(stmt).first()
        if result:
            return result

def query_all(stmt) -> Sequence | None:
    with Session(engine) as session:
        result = session.scalars(stmt).all()
        if result:
            return result
        
def get_entry(id) -> model.ImageEntry | None:
    with Session(engine) as session:
        result = session.get(model.ImageEntry, id)
        if result:
            return result

def delete_entry(prim_key) -> None:
    with Session(engine) as session:
        entry = session.get(model.ImageEntry, prim_key)
        session.delete(entry)
        session.commit()

