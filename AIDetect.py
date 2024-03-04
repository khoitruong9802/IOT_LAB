from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
from dotenv import load_dotenv
import sys
import os

class AI:
    def __init__(self):
        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Load the model
        self.model = load_model("keras_model/keras_model.h5", compile=False)

        # Load the labels
        self.class_names = open("keras_model/labels.txt", "r").readlines()

        # CAMERA can be 0 or 1 based on default camera of your computer
        if load_dotenv(override=True):
            self.camera = cv2.VideoCapture(os.getenv("CAM_IP"))
        else:
            print("Fail to read from env")
            sys.exit(1)

    def run(self, callback=None):
        count = 0
        while True:
            # Grab the webcamera's image.
            ret, image = self.camera.read()

            # Resize the raw image into (224-height,224-width) pixels
            image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

            # Show the image in a window
            cv2.imshow("Webcam Image", image)

            if count == 200:
                count = 0
                # Make the image a numpy array and reshape it to the models input shape.
                image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

                # Normalize the image array
                image = (image / 127.5) - 1

                # Predicts the model
                prediction = self.model.predict(image)
                index = np.argmax(prediction)
                class_name = self.class_names[index]
                confidence_score = prediction[0][index]

                # Print prediction and confidence score
                print("Class:", class_name[2:], end="")
                print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
                if callback is not None:
                    callback(class_name.split(" ")[1])

            # Listen to the keyboard for presses.
            keyboard_input = cv2.waitKey(20)
            count = count + 1

            # 27 is the ASCII for the esc key on your keyboard.
            if keyboard_input == 27:
                break

    def __del__(self):
        self.camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    AI().run()
