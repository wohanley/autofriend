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
    return [image[y: y + height, x: x + width]
            for (x, y, width, height) in face_detector.detectMultiScale(
                image,
                minSize=(50, 50))]


def decode(imageData):
    # return cv2.imdecode(np.array(imageData), cv2.CV_LOAD_IMAGE_GRAYSCALE)
    return cv2.imdecode(
        np.asarray(bytearray(imageData), dtype=np.uint8),
        cv2.CV_LOAD_IMAGE_GRAYSCALE)


def prepare_image(filename):
    return cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)


def wohanley_updates():

    wohanley_path = 'resources/wohanley'
    updates = []

    for f in listdir(wohanley_path):
        path = join(wohanley_path, f)
        if isfile(path):
            updates.append((prepare_image(path), 1))

    return updates
