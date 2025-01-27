import cv2
REFERENCE_HAND_SIZE = 100
DEFAULT_SENSITIVITY = 4
DEFAULT_FPS = 60

CAMERA_CONFIG = {
    'width': 640,
    'height': 480,
    'fps': 15,
    'fourcc': cv2.VideoWriter_fourcc(*'MJPG'),
    'autofocus': 0
}