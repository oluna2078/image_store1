from typing import Annotated
from uuid import UUID
from fastapi import FastAPI, File, HTTPException, Path, Response
from fastapi.responses import FileResponse

from src import storage as storage
from src import image_handler as img_handler

FAVICON_PATH: str = "res/favicon.ico"

app = FastAPI()


@app.get("/favicon.ico", response_class=FileResponse)
def get_favicon():
    return FAVICON_PATH


@app.post("/media/")
def add_image(image_stream: Annotated[bytes, File()]):
    image = img_handler.stream2image(image_stream)
    if image:
        media_id: str = img_handler.save_image(image)
        return {"media_id": media_id}
    else:
        raise HTTPException(status_code=422, detail="Cannot process image")


@app.get(
    "/media/{id}",
    responses = {
        200: {
            "content": {
                "image/png": {},
                "image/jpeg": {},
                "image/webp": {},
                "image/gif": {},
                "image/x-icon": {}
            }
        }
    },
    response_class=Response
)
def view_image(
        id: Annotated[UUID, Path()]
):
    media_id: str = str(id)
    image = img_handler.get_image(media_id)

    if image:
        filetype: str = img_handler.get_filetype(media_id)
        mediatype: str = img_handler.get_mimetype(filetype)
        image_bytes = img_handler.image2stream(image, filetype)

        return Response(content=image_bytes, media_type=mediatype)    
    else:
        raise HTTPException(status_code=404, detail="File not found")
