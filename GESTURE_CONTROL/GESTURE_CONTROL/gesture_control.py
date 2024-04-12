from ..CAPTURE_DETECT.capture_detect import CAPTURE_AND_DETECT
from ..GESTURE_PROCESSOR.gesture_processor import GESTURE_PROCESSOR

#$$$$$$$$$$#

class GESTURE_CONTROL :
    def __init__(self) -> None :
        self.PROCESSOR = GESTURE_PROCESSOR()
        self.CAPTURER = CAPTURE_AND_DETECT()

        self.CAPTURER.add_gesture_processing_object_ref(self.PROCESSOR)

    def start(self) -> None :
        self.CAPTURER.start()

    def stop(self) -> None :
        self.CAPTURER.stop()
