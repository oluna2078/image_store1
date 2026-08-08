from typing import Annotated
from PIL.ImageFile import ImageFile
from fastapi import FastAPI, File, Path, Response, UploadFile
import uuid
from io import BytesIO
from PIL import Image

from src import storage as storage
from src import database as db


app = FastAPI()


@app.post("/media/")
def save_image(
        image_stream: Annotated[bytes, File()]
) -> str:
    image: ImageFile = Image.open(BytesIO(image_stream))
    id: str = storage.store_image(image)
    db.index_image(image, id)

    return id


@app.get(
    "/media/{media_id}",
    responses = {
        200: {
            "content": {"image/png": {}}
        }
    },
    # Prevent FastAPI from adding "application/json"
    # as an additional response type
    response_class=Response
)
def read_image(
        media_id: Annotated[str, Path()]
):
    image: ImageFile = storage.retrieve_image(media_id)
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    image_bytes = buffer.getvalue()

    return Response(content=image_bytes, media_type="image/png")    
