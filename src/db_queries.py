from sqlalchemy import select
from sqlalchemy.sql.selectable import Select

from src import db_models as model


def id(id: str) -> Select:
    stmt = (
        select(model.ImageEntry.id)
        .where(model.ImageEntry.id == id)
    )
    return stmt


def filetype(id: str) -> Select:
    stmt = (
        select(model.ImageEntry.filetype)
        .where(model.ImageEntry.id == id)
    )
    return stmt


def metadata(id: str) -> Select:
    stmt = (
        select(model.ImageEntry.image_metadata)
        .where(model.ImageEntry.id == id)
    )
    return stmt


def hash(hash: str) -> Select:
    stmt = (
        select(model.ImageEntry.id)
        .where(model.ImageEntry.hash == hash)
    )
    return stmt


# Searches for all ImageEntries with [hash] which aren't duplicates
def hash_not_duplicate(hash: str) -> Select:
    stmt = (
        select(model.ImageEntry.id)
        .where(model.ImageEntry.hash == hash)
        .where(model.ImageEntry.duplicate_of == None)
    )
    return stmt

