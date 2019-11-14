import os
from io import BytesIO
from flask import Flask, send_from_directory, send_file, request, jsonify
from flask_pymongo import PyMongo
from PIL import Image
import numpy as np
import time
import subprocess
from skimage.filters import gaussian
from skimage.transform import rescale,rotate
from skimage.util import img_as_ubyte
dirpath = os.getcwd()
from zipfile import ZipFile

app = Flask(__name__, static_url_path='/static', static_folder = "./frontend/public")

app.config['MONGO_URI'] = "mongodb://%s:27017/main"%(os.environ['DB_PORT_27017_TCP_ADDR'])
mongo = PyMongo(app)

# create image and log collections
images_collections = mongo.db.images
images_collections.drop()
logs_collections = mongo.db.logs

def display_array(arr):
    """
    Display an image represented as an array
    """
    img = Image.fromarray(arr.astype(np.uint8))
    bytesIO = BytesIO()
    img.save(bytesIO, 'PNG')
    bytesIO.seek(0)
    return bytesIO

def convert_to_array(path):
    """
    Converts an image file to an array for later processing
    """
    image_file = Image.open(path).convert("RGB")
    image_array = np.array(image_file)
    return image_array

@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def base(path):
    return send_from_directory('frontend/public', 'index.html')


@app.route("/api/populate_database", methods=['GET'])
def populate_database():
    """
    Finds all images files of type `.png` inside the `assets` folder and for each image,
    inserts into the database `images` collection a document with the following fields:
    `file_name, width, height, area, size_bytes`

    question 1 & question 2
    """
    folder_path = "./assets/"
    # go through all .png files in the assets folder
    for image_name in os.listdir(folder_path):
        image = Image.open(folder_path+image_name)
        width,height = image.size
        area = width * height
        size = os.path.getsize(folder_path+image_name)
        # insert avoid duplicate
        images_collections.update({"imagename":image_name},{"imagename":image_name,"width":width, "height":height, "area": area, "size":size},True)

    # create a mongoDB index on the collection
    images_collections.create_index("_id")
    return jsonify("")

@app.route("/api/all", methods=['GET'])
def get_image_attributes():
    """
    Serves the contents of the `images` collection in a tabular format

    question 3
    """
    result = []
    for data in images_collections.find():
        data['_id'] = str(data['_id'])
        result.append(data)
    return jsonify(result)

@app.route("/api/query", methods=["GET"])
def query():
    """
    Serves a list of all available image file names, that match query params

    question 4
    """
    max_width = request.args.get('max_width')
    min_area = request.args.get('min_area')
    min_bits_per_pix = request.args.get('min_bits_per_pix')

    file_names_cursors = images_collections.find({
        "width": { "$lte": int(max_width)},
        "area": {"$gte": int(min_area)},
    },{"imagename":1, "size":1 ,"area":1 ,"_id":0})

    file_names = []
    for file_names_cursor in file_names_cursors:
        value = file_names_cursor["area"] / file_names_cursor["size"]
        if value >= int(min_bits_per_pix):
            file_names.append(file_names_cursor["imagename"])
    return jsonify(file_names)


@app.route("/api/filter/<imagename>/<filtertype>", methods=["GET"])
def image_filters(imagename,filtertype):
    """
    Perform all image processing operations
    :param imagename: the image name
    :param filtertype: the operations
    :return: the converted image

    Question 5
    """
    starttime = time.time()
    image_path = dirpath+"/assets/"+imagename+".png"
    image_array = convert_to_array(image_path)
    image_converted_array = None

    if filtertype == "original":
        image_converted_array = image_array

    # set dx to perform grayscale
    elif filtertype == "dx":
        image_file = Image.open(image_path).convert("L")
        image_converted_array = np.array(image_file)

    elif filtertype == "lowpass":
        image_converted_array = img_as_ubyte(gaussian(image_array,sigma=float(request.args.get('value'))))

    elif filtertype == "crop":
        image_converted_array = image_filters_crop(image_path)

    elif filtertype == "downsample":
        rate = 1/float(request.args.get('value'))
        image_converted_array = img_as_ubyte(rescale(image_array, rate))

    elif filtertype == "rotate":
        degree = -float(request.args.get('value'))
        image_converted_array = img_as_ubyte(rotate(image_array, degree, resize=True))

    # set it to perform power_spectrum
    elif filtertype == "dy":
        image_converted_array = image_filters_power_spectrum(image_path)
    image_converted = display_array(image_converted_array)
    processing_time = time.time() - starttime

    logs_collections.insert({"filename":imagename, "filtertype": filtertype, "request_timestamp": starttime, "processing_time": processing_time})

    return send_file(image_converted, mimetype='image/png')


def image_filters_power_spectrum(image_path):
    """
    Do power_spectrum of the image
    :param image_path: the file path
    :return: the array after converting

    Question 5 - 8
    """
    image_array = image_filters_crop(image_path)
    fourier_image_array = np.fft.fft(image_array)
    square = np.abs(fourier_image_array) ** 2
    maxnum = np.max(square);
    minnum = np.min(square);
    scale =  255/(maxnum - minnum)
    square = square * scale
    return np.clip(square, 0, 255)

def image_filters_normalize(image_path):
    """
    Do normalize of the image
    :param image_path: the file path
    :return: the array after converting

    Question 5 - 7
    """
    image_array = convert_to_array(image_path)
    patch_means = []
    patch_stds = []

    for i in range(0, image_array.shape[1], 32):
        for j in range(0, image_array.shape[0], 32):
            patch = image_array[j:j + 32, i:i + 32:]
            patch_means.append(np.mean(patch))
            patch_stds.append(np.std(patch))

    u = np.median(patch_means)
    v = np.median(patch_stds)
    minnum = u-3*v
    maxnum = u+3*v
    if minnum-3*v < 0:
        minnum = abs(minnum)
    if maxnum > 255:
        maxnum = 255 - abs(maxnum- 255)
    image_array = np.clip(image_array, minnum, maxnum)

    return image_array


def image_filters_crop(image_path):
    """
    Do centre crop of the image
    :param image_path: the file path
    :return: the array after converting

    Question 5 - 4
    """
    image_array = convert_to_array(image_path)
    width = image_array.shape[0]
    height = image_array.shape[1]
    length = min(width, height)
    start_x = width // 2 - length // 2
    start_y = height // 2 - length // 2
    image_array_converted = image_array[start_x:(start_x + length), start_y:(start_y + length), :]
    return image_array_converted

@app.route("/api/log", methods=['GET'])
def log():
    """
    List the 100 most recent image requests

    Question 6
    """
    logs = list(logs_collections.find().limit(100))
    result = []
    for data in logs:
        data['_id'] = str(data['_id'])
        result.append(data)
    return jsonify(result)

@app.route("/api/backup",methods=['GET'])
def backup():
    """
    backup the images from assets, zip them, and store it to backups folder by creat time

    Question 8
    """
    if not os.path.exists("backups"):
        os.makedirs("backups")
    currtime = time.time()
    # Cannot find zip in the docker, I tried in my local environment and it worked
    # for image_name in os.listdir('./assets'):
    #     process = subprocess.Popen(["zip", dirpath+'/backups/backup_' + str(currtime) + '.zip', dirpath+'/assets/' + image_name],shell=True)
    #     process.wait()

    ##alternative by using ZipFile
    with ZipFile(dirpath+'/backups/backup_' + str(currtime) + '.zip', 'w') as zip:
        for image_name in os.listdir('./assets'):
            zip.write(dirpath+'/assets/' + image_name)
    return jsonify("")

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)