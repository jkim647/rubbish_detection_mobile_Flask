from flask import Flask, redirect, url_for, request, render_template,jsonify
import tensorflow as tf
import cv2
from werkzeug.utils import secure_filename
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'


app = Flask(__name__)

CATEGORIES = ["Bottle", "Can"]
def prepare(filepath):
    IMG_SIZE = 50
    img_array = cv2.imread(filepath,cv2.IMREAD_GRAYSCALE)
    img_array = img_array / 255.0
    new_array = cv2.resize(img_array,(IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predictPlastic', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            basepath = os.path.dirname(__file__)
            file_path = os.path.join(
                basepath, 'upload', secure_filename(file.filename))
            file.save(file_path)
            model = tf.keras.models.load_model("64x3-CNN.h5")
            prediction = model.predict([prepare(file_path)])
            print(prediction)
            return CATEGORIES[int(prediction[0][0])]

@app.route('/predictCode', methods=['GET', 'POST'])
def predict():
    

if __name__ == '__main__':
    app.run()