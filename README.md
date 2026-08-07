# Image store /w API

Using normal filestor structure for the moment. The files are stored in `./files/{id}`. The plan is to get a file storage system, a database that keeps track of these files and an API that interacts with both up and running.

```
file storage <- database <- API
```

It would be useful to add Docker later and other things to at least make it fit to host on Kubernetes/Podman.


### Storage
The structure is the following:
```
./files/{media_id}
```

`{media_id}` is the file name.

goals:
-[ ] function: `image.filetype` -> `media_id` (save)
-[ ] function: `media_id` -> `image[media_id]` (retrieve)
-[ ] validation of files (if they are valid images, aybe via MIME types)
-[ ] autoconversion to a standard filetype for all images (e.g. all to JPEG)
-[ ] compression before storing images (maybe using ffmpeg)
-[ ] removal of EXIF data (maybe using exiftool)


### Database
`{media_id}` as the primary key with filetype & metadata in different columns.
The media id may be a standard form UUID

goals:
-[ ] function: `image.filetype, metadata` -> `media_id` (insert)
-[ ] function: `media_id` -> `image.filetype, metadata` (select)


### API
URL structure:
```
http://domain.test/media/{media_id}.filetype
```

goals:
-[ ] function: `image.filetype, metadata` -> `image_url` (store)
-[ ] function: `image_url` -> `image.filetype` (read)


##### Furthermore
I might need to make everything async...
