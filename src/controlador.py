import cv2
import time
from modelo import HandDetector, GestureProcessor, draw_landmarks_on_image
from config import CAMERA_CONFIG, DEFAULT_FPS

class AppController:
    def __init__(self, view):
        self.view = view
        self.cap = cv2.VideoCapture(0)
        self._setup_camera()
        self.detector = HandDetector()
        self.gesture_processor = GestureProcessor()
        self.fps = DEFAULT_FPS
        self.frame_time = 1/self.fps
        self.last_frame_time = 0
        self.start()
    
    def _setup_camera(self):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_CONFIG['width'])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_CONFIG['height'])
        self.cap.set(cv2.CAP_PROP_FPS, CAMERA_CONFIG['fps'])
        self.cap.set(cv2.CAP_PROP_FOURCC, CAMERA_CONFIG['fourcc'])
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, CAMERA_CONFIG['autofocus'])
    
    def start(self):
        self.update_frame()
    
    def update_frame(self):
        current_time = time.time()
        if current_time - self.last_frame_time >= self.frame_time:
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                detection_result = self.detector.detect(frame_rgb)
                annotated_image, hand_measurements = draw_landmarks_on_image(frame_rgb, detection_result)
                self.gesture_processor.process_gestures(hand_measurements)
                self.view.update_frame(annotated_image)
                self.last_frame_time = current_time
        
        self.view.window.after(int(self.frame_time * 1000), self.update_frame)
    
    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()