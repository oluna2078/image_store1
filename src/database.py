from typing import Optional
from sqlalchemy import JSON, engine, create_engine, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column
import os


class Base(DeclarativeBase):
    pass

class ImageEntry(Base):
    __tablename__ = "images"
    id: Mapped[str] = mapped_column(primary_key=True)
    filetype: Mapped[str]
    image_metadata: Mapped[Optional[list[str]]] = mapped_column(JSON)


DB_PATH: str = os.getcwd() + "/db"

# creates ../db if needed
def init_db_dir() -> None:
    try:
        os.mkdir(DB_PATH, mode=0o700)
    except FileExistsError:
        print(f"{DB_PATH} already exists, init skipped")

init_db_dir()


engine = create_engine(f"sqlite:///{DB_PATH}/media-index.sqlite3", echo=False)

Base.metadata.create_all(engine)


# takes PIL image obj, str with UUID
# returns store_id (in UUID) as str
def index_image(image, id) -> str:
    with Session(engine) as session:
        image_format = image.format
        entry = ImageEntry(id=id, filetype=image_format)

        session.add(entry)
        session.commit()

        return id

# takes media_id (str) and checks if db contains it
# returns boolean
def image_exists(media_id: str) -> bool:
    with Session(engine) as session:
        stmt = select(ImageEntry).where(ImageEntry.id == media_id)
        exists = session.scalars(stmt).first()

        if exists:
            return True
        else:
            return False

# takes media_id and queries for file format
def get_filetype(media_id: str) -> str:
    with Session(engine) as session:
        stmt = select(ImageEntry.filetype).where(ImageEntry.id == media_id)
        filetype = session.scalars(stmt).first()
        if filetype:
            return filetype
        else:
            raise NoResultFound
