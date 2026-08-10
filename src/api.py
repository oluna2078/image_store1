from typing import Annotated
from uuid import UUID
from fastapi import FastAPI, File, HTTPException, Path, Response
from fastapi.responses import FileResponse, HTMLResponse

from src import storage as storage
from src import image_handler as img_handler

FAVICON_PATH: str = "res/favicon.ico"

app = FastAPI()


# tab icon
@app.get("/favicon.ico", response_class=FileResponse)
def get_favicon():
    return FAVICON_PATH


# uploads
@app.post("/media/upload/")
def add_image(image_stream: Annotated[bytes, File()]):
    image = img_handler.stream2image(image_stream)
    if image:
        media_id: str = img_handler.save_image(image)
        return {"media_id": media_id}
    else:
        raise HTTPException(status_code=422, detail="Cannot process image")

@app.post("/media/multi-upload/")
def add_multiple_images(image_list: Annotated[list[bytes], File()]):
    media_ids: list[dict[str, str]] = []

    for image_stream in image_list:
        image = img_handler.stream2image(image_stream)
        if image:
            media_id: str = img_handler.save_image(image)
            media_ids.append({"media_id": media_id})
        else:
            raise HTTPException(status_code=422, detail="Cannot process image")

    return media_ids


# downloads
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


@app.get("/")
async def main():
    content = """
        <body>
            <h2>Upload an image:</h2>
            <form action="/media/upload/"
                  enctype="multipart/form-data"
                  method="post">
                <input name="image_stream" type="file" multiple>
                <input type="submit">
            </form>
            <hr>
            <h2>Upload multiple images:</h2>
            <form action="/media/multi-upload/"
                  enctype="multipart/form-data"
                  method="post">
                <input name="image_list" type="file" multiple>
                <input type="submit">
            </form>
            <hr>
            <h2>View images:</h2>
            <p>Go to <a href=/media/>/media/{id}</a> and type the id afterwards.</p>
        </body>
    """
    return HTMLResponse(content=content)
