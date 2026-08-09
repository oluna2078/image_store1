# Image store /w API

![Big logo image][logo]

Using normal filestore structure for the moment. The files are stored in `./store/{id}`. The plan is to get a file storage system, a database that keeps track of these files and an API that interacts with both up and running.

```
file storage <- database <- API
```


### Storage
The structure is the following:
```
./files/{media_id}
```

`{media_id}` is the file name.

goals:
- [x] function: `image.filetype` -> `media_id` (store)
- [x] function: `media_id` -> `image[media_id]` (retrieve)
- [x] validation of files (if they are valid images, maybe via MIME types)
    atm done via PIL/Pillow
- [ ] autoconversion to a standard filetype for all images (e.g. all to JPEG)
- [ ] compression before storing images (maybe using ffmpeg)
- [ ] removal of EXIF data (maybe using exiftool)


### Database
`{media_id}` as the primary key with filetype & metadata in different columns.
The media id may be a standard form UUID

goals:
- [x] function: `image.filetype, (metadata)` -> `media_id` (index)
- [ ] add metadata processing


### API
URL structure:
```
http://domain.test/media/{media_id}
```

goals:
- [x] function: `image.filetype, metadata` -> `image_url` (save)
- [x] function: `image_url` -> `image.filetype` (read)


## Furthermore
I might need to make everything async...

It would be useful to add Dockerfile later and other things to at least make it fit to host on Kubernetes/Docker.

[logo]: ./res/image_store1_logo.png
