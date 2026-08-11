from io import BytesIO
from PIL import Image
from PIL.ImageFile import ImageFile
from sqlalchemy import except_
from sqlalchemy.exc import NoResultFound

from src import storage as storage
from src import database as db
from src import db_queries as queries


PREFFERED_FORMAT: str = ''

MIME_TYPES: dict[str, str] = {
    'PNG': 'image/png',
    'JPEG': 'image/jpeg',
    'WEBP': 'image/webp',
    'GIF': 'image/gif',
    'ICO': 'image/x-icon'
}

DEFAULT_TYPE: str = 'image/png'


# converts bytestream into image
def stream2image(stream: bytes) -> ImageFile | None:
    try:
        image: ImageFile = Image.open(BytesIO(stream))
        return image
    except:
        return None

# converts image into bytestream with format:filetype
def image2stream(image: ImageFile, filetype: str) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format=filetype)
    stream = buffer.getvalue()
    return stream


# takes an image, indexes and stores it
# gives back its media_id
def save_image(image) -> str:
    id: str = storage.store_image(image)
    db.index_image(image, id)
    return id

## Checks if image exists and returns a boolean
def image_exists(media_id: str) -> bool:
    exists = db.query(queries.id(media_id))
    if exists:
        return True
    else:
        return False

# takes media_id and returns image file
def get_image(media_id: str) -> ImageFile | None:
    if image_exists(media_id):
        image: ImageFile = storage.retrieve_image(media_id)
        return image    

# takes media_id and deletes requested image
# returns None if successful and a str with details if not
def delete_image(media_id: str) -> str | None:
    if image_exists(media_id):
        db.delete_entry(media_id)

        try:
            storage.delete_file(media_id)
        except:
            return "Deletion failed"
    else:
        return "Image not found"

# queries the filetype of an image
def get_filetype(media_id: str) -> str:
    filetype = db.query(queries.filetype(media_id))
    if filetype:
        return filetype
    else:
        raise NoResultFound

# takes filetype and outputs MIME type
# if the filetype isn't known it returns a default
def get_mimetype(filetype: str) -> str:
    if filetype in MIME_TYPES:
        return MIME_TYPES[filetype]
    else:
        return DEFAULT_TYPE


