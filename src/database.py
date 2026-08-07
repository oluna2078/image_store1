from typing import Optional

from sqlalchemy import String, engine, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column

engine = create_engine("sqlite:///media-ids.sqlite3", echo=True)

class Base(DeclarativeBase):
    pass

class Images(Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(primary_key=True)
    filetype: Mapped[str]
    image_metadata: Mapped[Optional[str]]

Base.metadata.create_all(engine)


