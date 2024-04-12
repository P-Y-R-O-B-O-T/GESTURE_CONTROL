import cv2
import threading
import time
import mediapipe as mp

#$$$$$$$$$$#

FACE = mp.solutions.face_detection.FaceDetection()
HANDS = mp.solutions.hands.Hands(min_detection_confidence = 0.6,
                                 min_tracking_confidence=0.5)
HOLLISTIC = mp.solutions.holistic.Holistic()

DRAWING = mp.solutions.drawing_utils

VIDEO_CAPTURE = cv2.VideoCapture(0)

#$$$$$$$$$$#

class CAPTURE_AND_DETECT :
    def __init__(self,
                 cam_inp_device: int=0) -> None :
        global VIDEO_CAPTURE
        self.STATUS = True

        self.CAM_WIDTH = VIDEO_CAPTURE.get(3)
        self.CAM_HEIGHT = VIDEO_CAPTURE.get(4)

        if cam_inp_device > 0 :
            VIDEO_CAPTURE = cv2.VideoCapture(cam_inp_device)

    def capture_and_detection_loop(self) -> None :
        global VIDEO_CAPTURE
        while self.STATUS :
            i = time.time()
            success_code, frame = VIDEO_CAPTURE.read()

            frame = cv2.flip(frame, 1)

            #frame = cv2.resize(frame,
            #                   (256, 256))

            frame = cv2.cvtColor(frame,
                                 cv2.COLOR_BGR2RGB)

            face_res = None #FACE.process(frame)
            hands_res = HANDS.process(frame)

            hollistic_res = None #HOLLISTIC.process(frame)

            frame = cv2.cvtColor(frame,
                                 cv2.COLOR_RGB2BGR)

            self.GESTURE_PROCESSOR.process_gesture({"face": face_res,
                                                    "hands": hands_res,
                                                    "hollistic": hollistic_res,
                                                    "camera_dimentions": {"height": self.CAM_HEIGHT,
                                                                          "width": self.CAM_WIDTH}})
            #if face_res.detections :
            #    for detection in face_res.detections :
            #        DRAWING.draw_detection(frame,
            #                               detection)

            if hands_res.multi_hand_landmarks :
                for hand_landmarks in hands_res.multi_hand_landmarks :
                    DRAWING.draw_landmarks(frame,
                                           hand_landmarks,
                                           mp.solutions.hands.HAND_CONNECTIONS)

            t = time.time()-i
            print(t)
            #DRAWING.draw_landmarks(frame,
            #                       hollistic_res.face_landmarks)

            #cv2.imshow("GESTURE", frame)
            #if cv2.waitKey(5) & 0xFF == ord("q") :
            #    break

    def add_gesture_processing_object_ref(self,
                                          gesture_processor: object) -> None :
        self.GESTURE_PROCESSOR = gesture_processor

    def start(self) -> None :
        self.MAIN_THREAD = threading.Thread(target=self.capture_and_detection_loop)
        self.MAIN_THREAD.start()

    def stop(self) -> None :
        self.STATUS = False
