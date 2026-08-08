import os, uuid
from PIL import Image


storage_path: str = os.getcwd() + "/store"

# creates ../store if needed
def init_store() -> None:
    try:
        os.mkdir(storage_path, mode=0o700)
    except FileExistsError:
        print(f"{storage_path} already exists, init skipped")


# takes an image and stores it in ../files/ with the file name: media_id
# returns filepath of stored image
def store_image(image) ->  str:
    media_id = uuid.uuid4()
    save_path = f"{storage_path}/{media_id}"
    image_format = image.format

    try:
        image.save(save_path, image_format)
        os.chmod(save_path, 0o600)
        return str(media_id)
    except OSError as err:
        raise OSError(err)

# takes media_id as str
# returns PIL image obj from store
def retrieve_image(media_id):
    image = Image.open(f"{storage_path}/{media_id}")

    return image
