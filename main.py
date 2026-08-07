import src.storage as storage
import src.database as db

from PIL import Image

storage.init_store()
print(storage.store_image(Image.open("./test-image.png"), "bi32r732g3g2uh37738ih"))
print(storage.store_image(Image.open("./test-image2.png"), "hkwje42fweofnF384324r"))
