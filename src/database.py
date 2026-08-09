from sqlalchemy import engine, create_engine, select
from sqlalchemy.exc import NoResultFound
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
def index_image(image, id) -> str:
    with Session(engine) as session:
        image_format = image.format
        entry = model.ImageEntry(id=id, filetype=image_format)

        session.add(entry)
        session.commit()

        return id

# takes media_id and queries for file format
def query(stmt) -> str | None:
    with Session(engine) as session:
        result = session.scalars(stmt).first()
        if result:
            return result

