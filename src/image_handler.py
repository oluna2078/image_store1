from io import BytesIO
from PIL import Image
from PIL.ImageFile import ImageFile
from sqlalchemy.exc import NoResultFound

from src import storage as storage
from src import database as db
from src import db_queries as queries


PREFFERED_FORMAT: str = ''


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


# takes media_id and returns image file
def get_image(media_id: str) -> ImageFile | None:
    if db.query(queries.id(media_id)):
        image: ImageFile = storage.retrieve_image(media_id)
        return image    

# queries the filetype of an image
def get_filetype(media_id: str) -> str:
    filetype = db.query(queries.filetype(media_id))
    if filetype:
        return filetype
    else:
        raise NoResultFound


## Checks if image exists and returns a boolean
#def image_exists(media_id: str) -> bool:
#    exists = db.query(queries.id(media_id))
#    if exists:
#        return True
#    else:
#        return False
