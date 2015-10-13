import cv2
import numpy as np
from os import listdir
from os.path import isfile, join


def flatten(nested_list):
    return [item for sublist in nested_list for item in sublist]


def load_face_detector():
    return cv2.CascadeClassifier(
        'resources/haarcascade_frontalface_default.xml')


def face_regions(face_detector, image):

    return face_detector.detectMultiScale(
        image,
        scaleFactor=1.3,
        minNeighbors=8,
        minSize=(20, 20))


def prepare_image(filename):
    return cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)


def load_face_recognizer():

    recognizer = cv2.createLBPHFaceRecognizer()

    if isfile(recognizer_path):
        recognizer.load(recognizer_path)

    return recognizer

recognizer_path = 'resources/recognizer'


def update_recognizer(recognizer, updates):
    recognizer.update(
        np.array([image for (image, _) in updates]),
        np.array([label for (_, label) in updates]))


def wohanley_updates():

    wohanley_path = 'resources/wohanley'
    updates = []
    
    for f in listdir(wohanley_path):
        path = join(wohanley_path, f)
        if isfile(path):
            updates.append((prepare_image(path), 1))

    return updates
