import cv2
import numpy as np
from os.path import isfile


class FaceRecognizer():

    recognizer_path = 'resources/recognizer'

    def __init__(self):

        self.recognizer = cv2.createLBPHFaceRecognizer()

        if isfile(self.recognizer_path):
            self.recognizer.load(self.recognizer_path)

    def update(self, updates):

        self.recognizer.update(
            np.array([image for (image, _) in updates]),
            np.array([label for (_, label) in updates]))

        self.recognizer.save(self.recognizer_path)

    def recognize_face(self, region):
        return self.recognizer.predict(region)
