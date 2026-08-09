from sqlalchemy import select
from sqlalchemy.sql.selectable import Select

from src import db_models as model


def id(id: str) -> Select:
    stmt = select(model.ImageEntry.id).where(model.ImageEntry.id == id)
    return stmt

def filetype(id: str) -> Select:
    stmt = select(model.ImageEntry.filetype).where(model.ImageEntry.id == id)
    return stmt

def metadata(id: str) -> Select:
    stmt = select(model.ImageEntry.metadata).where(model.ImageEntry.id == id)
    return stmt
