import os
from flask import Flask, render_template, request
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename
import config

from scene import SceneDetection


# Make the scene recognizer object
scene_recognizer = SceneDetection(config.MODEL_PATH)

# Create path to save uploaded images
save_path = config.UPLOAD_PATH
os.makedirs(save_path, exist_ok=True)

# Create flask application
app = Flask(__name__, static_folder=save_path, static_url_path='/image')


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      filename = secure_filename(f.filename)
      f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
      print("file saved")
      return render_template('result.html', image_link="http://localhost:5000/image/{}".format(filename), detected_scene="test")


if __name__=='__main__':
    app.run(debug=True)
