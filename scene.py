import numpy as np
import cv2
import tensorflow
import logging


class SceneDetection:

    def __init__(self, model_path, input_size=(224,224), classes=['cloudy', 'rainy', 'sunrise', 'sunshine']):
        self.model_path = model_path
        self.input_size = input_size
        self.classes = classes
        self.model = tensorflow.keras.models.load_model(model_path)


    def preprocess(self, img_path):
        try:
            image = cv2.imread(img_path)
            image = cv2.resize(image, (224,224))
            inputs = np.expand_dims(image, 0)
        except Exception as e:
            logging.error("Exception occured while pre processing image")
            logging.error(e)
            return None

        return inputs


    def get_class_name(self, output):
        try:
            return self.classes[np.argmax(output)]
        except Exception as e:
            logging.error("Exception occured while post processing")
            logging.error(e)
            return None


    def predict(self, img_path):
        
        inputs = self.preprocess(img_path)
        if inputs is None:
            return False, "input error"          #status, data

        try:
            output = self.model.predict(inputs)[0]
        except Exception as e:
            logging.error("error while doing model prediction")
            logging.error(e)
            return False, "prediction error"

        class_name = self.get_class_name(output)
        if class_name is None:
            return False, "postprocessing error"

        return True, class_name


if __name__=='__main__':
    model = SceneDetection('weights/scene_model.h5')
    output = model.predict('test/sunny.jpeg')
    print(output)
