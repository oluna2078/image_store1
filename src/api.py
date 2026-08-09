from typing import Annotated
from uuid import UUID
from PIL.ImageFile import ImageFile
from fastapi import FastAPI, File, HTTPException, Path, Response
from io import BytesIO
from PIL import Image
from fastapi.responses import FileResponse

from src import storage as storage
from src import database as db

FAVICON_PATH: str = "res/favicon.ico"

app = FastAPI()

@app.get("/favicon.ico", response_class=FileResponse)
def get_favicon():
    return FAVICON_PATH

@app.post("/media/")
def save_image(
        image_stream: Annotated[bytes, File()]
) -> str:
    image: ImageFile = Image.open(BytesIO(image_stream))
    id: str = storage.store_image(image)
    db.index_image(image, id)

    return id


@app.get(
    "/media/{id}",
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
        id: Annotated[UUID, Path()]
):
    media_id: str = str(id)
    if db.image_exists(media_id) is True:
        image: ImageFile = storage.retrieve_image(media_id)
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        image_bytes = buffer.getvalue()

        return Response(content=image_bytes, media_type="image/png")    
    else:
        raise HTTPException(status_code=404, detail="File not found")
