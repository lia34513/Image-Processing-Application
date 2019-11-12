import os
from io import BytesIO
from flask import Flask, send_from_directory, send_file
from flask_pymongo import PyMongo
from PIL import Image
import numpy as np

app = Flask(__name__, static_url_path='/static', static_folder = "./frontend/public")

app.config['MONGO_URI'] = "mongodb://%s:27017/main"%(os.environ['DB_PORT_27017_TCP_ADDR'])

mongo = PyMongo(app)

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

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
