import src.storage as storage
import src.database as db
import uvicorn

from PIL import Image


storage.init_store()

if __name__ ==  "__main__":
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)

