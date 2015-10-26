import core
import facerec


if __name__ == '__main__':

    detector = core.load_face_detector()
    recognizer = facerec.FaceRecognizer()

    img = core.prepare_image('resources/wohanley/panda.jpg')

    for (x, y, width, height) in core.face_regions(detector, img):
        print recognizer.recognize_face(img[y: y + height, x: x + width])
