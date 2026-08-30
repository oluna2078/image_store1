import uuid, hashlib
from io import BytesIO
from PIL import Image
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


# generates media_id and returns it as str
def generate_id() -> str:
    return str(uuid.uuid4())

# takes image and returns its hash as str
def hash_image(image: Image.Image) -> str:
    bytes = image.tobytes()
    hash = hashlib.sha1(bytes) # SHA-1 should be easier to compute
    return hash.hexdigest()


# converts bytestream into image
def stream2image(stream: bytes) -> Image.Image | None:
    try:
        image: Image.Image = Image.open(BytesIO(stream))
        return image
    except:
        return None

# converts image into bytestream with format:filetype
def image2stream(image: Image.Image, filetype: str) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format=filetype)
    stream = buffer.getvalue()
    return stream

# takes an image with its media_id, indexes and stores it
def save_image(media_id: str, image: Image.Image) -> None:
    hash = hash_image(image)
    original = db.query_first(queries.hash_not_duplicate(hash))

    if original:
        db.index_duplicate_image(image, media_id, hash, original)
    else:
        storage.store_image(image, media_id)
        db.index_new_image(image, media_id, hash)

# takes an image, indexes and stores it
# gives back its media_id
def save_new_image(image) -> str:
    media_id = generate_id()
    save_image(media_id, image)
    return media_id

# checks if image exists and returns a boolean
def image_exists(media_id: str) -> bool:
    exists = db.query_first(queries.id(media_id))
    if exists:
        return True
    else:
        return False

# takes media_id and returns image file
def get_image(media_id: str) -> Image.Image | None:
    entry = db.get_entry(media_id)
    if entry:
        if entry.duplicate_of:
            image: Image.Image = storage.retrieve_image(entry.duplicate_of)
            return image    
        else:
            image: Image.Image = storage.retrieve_image(media_id)
            return image    

# takes media_id and deletes requested image
# returns None if successful and a str with details if not
def delete_image(media_id: str) -> str | None:
    if image_exists(media_id):
        duplicates = db.query_all(queries.duplicate_of(media_id))
        if duplicates:
            duplicates_list: list = list(duplicates)
            new_origin = duplicates_list.pop(0)

            db.update_duplicate(id=new_origin, duplicate_of=None)
            for i in duplicates_list:
                db.update_duplicate(id=i, duplicate_of=new_origin)
            try:
                storage.rename_file(media_id, new_origin)
            except:
                return "Deletion failed"
        else:
            try:
                storage.delete_file(media_id)
            except:
                return "Deletion failed"
        db.delete_entry(media_id)
    else:
        return "Image not found"

# takes media_id and deletes requested image
# returns None if successful and a str with details if not
def update_image(media_id: str, new_image: Image.Image) -> str | None:
    if image_exists(media_id):
        if delete_image(media_id):
            return "Image not found"
        save_image(media_id, new_image)
    else:
        return "Image not found"


# queries the filetype of an image
def get_filetype(media_id: str) -> str:
    filetype = db.query_first(queries.filetype(media_id))
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


# adjust image ratio to wr:hr with minimal resolution loss
def crop_image(image: Image.Image,
               new_width: int|None = None,
               new_height: int|None = None
) -> Image.Image:
    width = image.size[0]
    height = image.size[1]

    # check if inputs are empty
    # after: check if new boundaries aren't bigger than the old ones
    if new_width == None:
        new_width = width
    elif new_width > width:
        new_width = width

    if new_height == None:
        new_height = height
    elif new_height > height:
        new_height = height
    
    # margins are used to crop around the center and not from a corner
    margin_h = (height - new_height) / 2
    margin_w = (width - new_width) / 2
    return image.crop((margin_w, margin_h, new_width + margin_w, new_height + margin_h))


# adjust image ratio to wr:hr with minimal resolution loss
def adjust_img_ratio(image: Image.Image, wr: int, hr: int) -> Image.Image:
    width = image.size[0]
    height = image.size[1]
    
    # try horizontal base
    new_height = width * (hr / wr)
    if new_height <= height:
        margin = (height - new_height) / 2
        return image.crop((0, margin, width, new_height + margin))
    # use vertical base
    else:
        new_width = height * (wr / hr)
        margin = (width - new_width) / 2
        return image.crop((margin, 0, new_width + margin, height))
    # margin is used to crop around the center and not from a corner


# scale image to either 1.0=100% (original) or less
def scale_image(image: Image.Image, scale: float) -> Image.Image:
    # I could scale both w and h but it would be wasted computation
    new_width = scale * image.size[0]
    image.thumbnail((new_width, image.size[1]))
    return image


# limit image w/h to max_w / max_h (in px)
def scale_image_limit(image: Image.Image,
               max_w: int|None = None,
               max_h: int|None = None
) -> Image.Image:
    # check if inputs are empty
    if max_w:
        new_max_w = max_w
    else:
        width = image.size[0]
        new_max_w = width
    if max_h:
        new_max_h = max_h
    else:
        height = image.size[1]
        new_max_h = height
    
    image.thumbnail((new_max_w, new_max_h))
    return image
