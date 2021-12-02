import os
from flask import Flask, render_template, request
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename

import logging
# Try other types of logging methods where you can define you own format and file size and naming parameters
logging.basicConfig(filename='logs/application.log', level=logging.DEBUG)

import config
from scene import SceneDetection


# Make the scene recognizer object
scene_recognizer = SceneDetection(config.MODEL_PATH)

# Create path to save uploaded images
save_path = config.UPLOAD_PATH
os.makedirs(save_path, exist_ok=True)

# Create flask application
app = Flask(__name__, static_folder=save_path, static_url_path='/image')
app.config['UPLOAD_FOLDER'] = save_path


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      filename = secure_filename(f.filename)
      filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
      f.save(filepath)

      status, result = scene_recognizer.predict(filepath)
      if not status:
          logging.error("error occured while processing the reuqest: \nError: '{}'".format(result))

      return render_template('result.html', image_link="http://localhost:5000/image/{}".format(filename), detected_scene=result)


if __name__=='__main__':
    app.run(debug=True)
