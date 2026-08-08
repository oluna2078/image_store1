from typing import Optional, List
from sqlalchemy import ARRAY, JSON, String, engine, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column
import os


class Base(DeclarativeBase):
    pass

class ImageEntry(Base):
    __tablename__ = "images"
    id: Mapped[str] = mapped_column(primary_key=True)
    filetype: Mapped[str]
    image_metadata: Mapped[Optional[list[str]]] = mapped_column(JSON)


db_path: str = os.getcwd() + "/db"

# creates ../db if needed
def init_db_dir() -> None:
    try:
        os.mkdir(db_path, mode=0o700)
    except FileExistsError:
        print(f"{db_path} already exists, init skipped")

init_db_dir()

engine = create_engine(f"sqlite:///{db_path}/media-index.sqlite3", echo=False)

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

