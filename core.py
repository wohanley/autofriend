import cv2
import os


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
    if os.path.isfile(recognizer_path):
        recognizer.load(recognizer_path)
    return recognizer

recognizer_path = 'resources/recognizer'


def update_recognizer(recognizer, updates):
    recognizer.update(
        [image for (image, _) in updates],
        [label for (_, label) in updates])
