import src.storage as storage
import src.database as db

from PIL import Image


def save_image(image) -> str:
    id: str = storage.store_image(image)
    db.index_image(image, id)

    return id

def get_image(id):
    image = storage.retrieve_image(id)

    return image


storage.init_store()

#print(save_image(Image.open("./test-image.png")))
#print(save_image(Image.open("./test-image2.png")))

get_image("4861cbce-d2ed-4fce-9c86-0fefc94245af").show()
