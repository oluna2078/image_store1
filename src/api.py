from typing import Annotated
from uuid import UUID
from fastapi import FastAPI, File, HTTPException, Path, Query, Response
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field

from src import storage as storage
from src import image_handler as img_handler

FAVICON_PATH: str = "res/favicon.ico"

app = FastAPI()


class ManipParams(BaseModel):
    model_config = {"extra": "forbid"}

    w: int | None = Field(None, gt=0)           # relative width
    h: int | None = Field(None, gt=0)           # relative height
                                                # > example: 3:2 => ?w=3&h=2
    s: float | None = Field(None, gt=0, le=1.0) # scale (1.0=100%)
    aw: int | None = Field(None, gt=0)          # absolute width (in px)
    ah: int | None = Field(None, gt=0)          # absolute height (in px)


def check_manip_q(manip_q_dict: dict) -> str|None:
    relative_sizing: bool = False
    absolute_sizing: bool = False
    if (manip_q_dict["w"]
        or manip_q_dict["h"]
        or manip_q_dict["s"]
    )!= None:
        relative_sizing = True

    if (manip_q_dict["aw"]
        or manip_q_dict["ah"]
    ) != None:
        absolute_sizing = True

    if (relative_sizing and absolute_sizing) == True:
        return "Cannot use relative and absolute sizing"


# uploads (single & multi)
@app.post("/media/upload/", status_code=201)
def add_image(image_stream: Annotated[bytes, File()]):
    image = img_handler.stream2image(image_stream)
    if image:
        media_id: str = img_handler.save_new_image(image)
        return {"media_id": media_id}
    else:
        raise HTTPException(status_code=415, detail="Cannot process image")

@app.post("/media/multi-upload/", status_code=201)
def add_multiple_images(image_list: Annotated[list[bytes], File()]
)-> list[dict[str, str]]:
    media_ids: list[dict[str, str]] = []

    for image_stream in image_list:
        image = img_handler.stream2image(image_stream)
        if image:
            media_id: str = img_handler.save_new_image(image)
            media_ids.append({"media_id": media_id})
        else:
            raise HTTPException(status_code=415, detail="Cannot process images")

    return media_ids


# downloads
@app.get(
    "/media/{id}",
    #responses = {
    #    200: {
    #        "content": {
    #            "image/png": {},
    #            "image/jpeg": {},
    #            "image/webp": {},
    #            "image/gif": {},
    #            "image/x-icon": {}
    #        }
    #    }
    #},
    #response_class=Response
)
def view_image(
        id: Annotated[UUID, Path()],                    # media id
        manip_query: Annotated[ManipParams, Query()]    # manipulation parameters
):
    media_id: str = str(id)
    image = img_handler.get_image(media_id)
    manip_q_dict: dict = dict(manip_query)
    manip_check = check_manip_q(manip_q_dict)

    if manip_check != None:
        raise HTTPException(status_code=400, detail=manip_check)

    if image:
        filetype: str = img_handler.get_filetype(media_id)
        mediatype: str = img_handler.get_mimetype(filetype)
        image_bytes = img_handler.image2stream(image, filetype)

        return Response(content=image_bytes, media_type=mediatype)    
    else:
        raise HTTPException(status_code=404, detail="File not found")


# delete
@app.delete("/media/{id}")
def delete_image(
        id: Annotated[UUID, Path()]
):
    details = img_handler.delete_image(str(id))
    if not details:
        return {"media_id": id}
    else:
        raise HTTPException(status_code=500, detail=f"Deletion failed: {details}")


# update/edit
@app.put("/media/{id}")
def update_image(
        id: Annotated[UUID, Path()],
        image_stream: Annotated[bytes, File()]
):
    new_image = img_handler.stream2image(image_stream)
    if new_image:
        details = img_handler.update_image(str(id), new_image)
        if not details:
            return {"media_id": id}
        else:
            raise HTTPException(status_code=500, detail=f"Update failed: {details}")
    else:
        raise HTTPException(status_code=415, detail="Cannot process images")


# tab icon
@app.get("/favicon.ico", response_class=FileResponse)
def get_favicon():
    return FAVICON_PATH


# small demo page
@app.get(
    "/",
    response_class=HTMLResponse
)
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
