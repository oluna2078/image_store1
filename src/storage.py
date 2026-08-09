from io import BytesIO
import os, uuid
from PIL import Image
from PIL.ImageFile import ImageFile


STORAGE_PATH: str = os.getcwd() + "/store"

# creates ../store if needed
def init_store() -> None:
    try:
        os.mkdir(STORAGE_PATH, mode=0o700)
    except FileExistsError:
        print(f"{STORAGE_PATH} already exists, init skipped")

init_store()


# takes an image and stores it in ../files/ with the file name: media_id
# returns filepath of stored image
def store_image(image) ->  str:
    media_id = uuid.uuid4()
    save_path = f"{STORAGE_PATH}/{media_id}"
    image_format = image.format

    image.save(save_path, image_format)
    os.chmod(save_path, 0o600)
    return str(media_id)

# takes media_id as str
# returns PIL image obj from store
def retrieve_image(media_id):
    image = Image.open(f"{STORAGE_PATH}/{media_id}")
    return image

