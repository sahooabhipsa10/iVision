import cv2
from imageai.Detection import ObjectDetection
import os
import pyttsx3


class VideoCamera(object):
    execution_path = os.getcwd()
    detector = ObjectDetection()
    detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath(os.path.join(execution_path, "yolo-tiny.h5"))
    detector.loadModel(detection_speed="flash")

    # buffer

    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()


    def speak(self, detections):
        for eachObject in detections:
            name = eachObject["name"]
            engine = pyttsx3.init()
            engine.say('I see ' + name)
            engine.runAndWait()

    def get_frame(self, flag):

        if flag == 1:
            engine = pyttsx3.init()
            engine.say('starting object detetction live stream.')
            engine.runAndWait()
            self.video = cv2.VideoCapture(0)

        ret, frame = self.video.read()

        detected_image_array, detections = self.detector.detectObjectsFromImage(input_type="array", input_image=frame,
                                                                                output_type="array",
                                                                                minimum_percentage_probability=30)

        self.speak(detections)

        ret, jpeg = cv2.imencode('.jpg', detected_image_array)
        return jpeg.tobytes()
