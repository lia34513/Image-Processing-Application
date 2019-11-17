# Image Processing Application

This repository contains the code required to deploy an image processing application. It is built using Svelte (front-end), Flask (Python-based API framework as the back-end) and MongoDB (persistent storage).

## Local Installation

- Build the stack: `docker-compose build`
- Run the stack: `docker-compose up`
- Remove the stack: `docker-compose down`
- Log in to the mongo shell when the container is running via `docker exec -it <container_id> mongo`
- Obtain `conainer_id` by running `docker ps`
- Application will start at `localhost:5000`

## API End Points

- `/api/populate_database`
    - Finds all images files of type `.png` inside the `assets` folder and for each image, inserts into the database `images` collection a document with the following fields:
    `file_name, width, height, area, size_bytes`
    
- `/api/all`
    - Serves the contents of the `images` collection in a tabular format
    
- `/api/query?max_width=X&min_area=Y&min_bits_per_pix=Z`
   - Serves a list of all available image file names, that match query params:
        - `max_width`: maximum width in pixels
        - `min_area`: minimum area in pixels
        - `min_bits_per_pix`: maximum size of image in bytes
        
- `/api/filter/<imagename>/<filtertype>?value=X`
    - Performs all image processing operations
        - `original`: return the original image as a png
        - `grayscale`: return the greyscale version of the image as a png
        - `lowpass`: return a low-pass filtered version of the image, with a Gaussian filter kernel, where the Gaussian standard deviation is *`value`* pixels. 
        - `crop`: return the largest possible square crop from the center of the image.
        - `downsample`: return a *`value`* downsampled version of the image (i.e. if value=1.5, the output is 1.5x smaller than the input). 
        - `rotate`: return a *`value`* degree clockwise rotated version of the image.
        - `normalize`: robust contrast normalization using patches
        - `power_spectrum`: the power spectrum of a image
        
- `/api/log`
    - List the 100 most recent image requests (`filename, filtertype, request_timestamp, processing_time`)
- `/api/backup`
    - zip of all the images in the `images` directory and store it in the `backups` directory.

## API Reference


- `server.populate_database()`

    - Inputs

    - Outputs

- `server.get_image_attributes()`

    - Inputs

    - Outputs
        - `response`: `list` of `dictionaries` (with keys `file_name, width, height, area, size_bytes`)

- `server.query()`

    - Inputs
        - `max_width`: `int`    
        - `min_area`: `int`
        - `min_bits_per_pix`: `int`

    - Outputs
        - `response`: `list` of `str`

- `server.image_filters(imagename, filtertype)`

    - Inputs
        - `imagename`: `str`
        - `filtertype`: `str`
        - `value`: `float`

    - Outputs

        - `response`: PNG file

- `server.log()`

    - Inputs

    - Outputs
        - `response`: List of dictionaries (with keys `filename, filtertype, request_timestamp, processing_time`)

- `server.backup()`

    - Inputs

    - Outputs
