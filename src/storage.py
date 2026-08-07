import os
from PIL import Image


storage_path: str = os.getcwd() + "/store"

# creates ../files if needed
def init_store() -> None:
    try:
        os.mkdir(storage_path, mode=0o700)
    except FileExistsError:
        print(f"{storage_path} already exists, init skipped")


# takes an image and stores it in ../files/ with the file name: media_id
# returns filepath of stored image
def store_image(image, store_id: str) ->  str:
    current_image = image
    save_path = f"{storage_path}/{store_id}"
    image_format = current_image.format

    try:
        current_image.save(save_path, image_format)
        return save_path
    except OSError:
        print("WARNING: cannot save image")
        return ""
