from typing import Optional
from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class ImageEntry(Base):
    __tablename__ = "images"
    id: Mapped[str] = mapped_column(primary_key=True)
    filetype: Mapped[str]
    image_metadata: Mapped[Optional[list[str]]] = mapped_column(JSON)

