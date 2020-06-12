# This is a _very simple_ example of a web service that recognizes faces in uploaded images.
# Upload an image file and it will check if the image contains a picture of Barack Obama.
# The result is returned as json. For example:
#
# $ curl -XPOST -F "file=@obama2.jpg" http://127.0.0.1:5001
#
# Returns:
#
# {
#  "face_found_in_image": true,
#  "is_picture_of_obama": true
# }
#
# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# NOTE: This example requires flask to be installed! You can install it with pip:
# $ pip3 install flask

import face_recognition
from flask import Flask, jsonify, request, redirect
from PIL import Image, ImageDraw
import cv2
import numpy as np
import base64
import io

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    data = {'success': False}
    if request.method == 'POST':
        # Check if a valid image file was uploaded
        if 'file' not in request.files:
            return jsonify(data)
        if not request.files.get('file'):
            return jsonify(data)
        file = request.files['file'].read()

        # if file and allowed_file(file.filename):
        if file:
            # The image file seems valid! Detect faces and return the result.
            file = io.BytesIO(file)
            locations, img = detect_faces_in_image(file)
            data['success'] = True
            data['prediction'] = locations
            # print(jsonify(result))
            # return img_stream
                # draw = ImageDraw.Draw(pil_img)
                # print(pil_img)
                # draw.polygon()
            # print(top, right, bottom, left)
            # return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:
    # print(data)
    return jsonify(data)


def detect_faces_in_image(file_stream):
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # pil_image = Image.fromarray(img)
    # pil_image.show()
    # Get face encodings for any faces in the uploaded image
    face_locations = face_recognition.face_locations(img)
    # print(face_locations)
    # return jsonify(result)
    return face_locations, img

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
