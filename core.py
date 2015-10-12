import cv2
from os import listdir
from os.path import isfile, join


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
    return cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2GRAY)


def load_face_recognizer():
    recognizer = cv2.createLBPHFaceRecognizer()
    if isfile(recognizer_path):
        recognizer.load(recognizer_path)
    return recognizer

recognizer_path = 'resources/recognizer'


def update_recognizer(recognizer, updates):
    recognizer.update(
        [image for (image, _) in updates],
        [label for (_, label) in updates])


def wohanley_updates():
    wohanley_path = 'resources/wohanley'
    for f in listdir(wohanley_path):
        path = join(wohanley_path, f)
        if isfile(path):
            yield (prepare_image(path), 'wohanley')
