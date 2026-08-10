# Simple image store API

![Big logo image][logo]

Using normal filestore structure for the moment. The files are stored in `./store/{id}`. The plan is to get a file storage system, a database that keeps track of these files and an API that interacts with both up and running.

```
file storage <- database <- API
```


### Storage
The directory structure is the following:
```
./store/{media_id}
```

`{media_id}` is the file name.

goals:
- [x] validation of files (if they are valid images, maybe via MIME types)
    atm done via PIL/Pillow
- [ ] autoconversion to a standard filetype for all images (e.g. all to JPEG)
- [ ] compression before storing images (maybe using ffmpeg)
- [ ] removal of EXIF data (maybe using exiftool)
- [ ] image processing like cropping/resizing etc.
- [ ] remove duplicates\*


### Database
`{media_id}` as the primary key with filetype & metadata in different columns.
The media id may be a standard form UUID

goals:
- [x] function: `image.filetype, (metadata)` -> `media_id` (index)
- [ ] add metadata processing
- [ ] save upload date
- [ ] \*duplicates are marked with a reference to the original


### API
Endpoints:
```
POST /media/upload/
POST /media/multi-upload/
GET  /media/{media_id}
```

goals:
- [ ] use `UploadFile` instead of `bytes`


## Furthermore
- I might need to make everything async...

- It would be useful to add Dockerfile later and other things to at least make it fit to host on Kubernetes/Docker.

- adding tests would be great

[logo]: ./res/image_store1_logo.png
