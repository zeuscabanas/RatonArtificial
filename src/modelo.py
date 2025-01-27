from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import cv2
from config import REFERENCE_HAND_SIZE, DEFAULT_SENSITIVITY
import pyautogui

class HandDetector:
    def __init__(self, model_path='hand_landmarker.task'):
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=2,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
    
    def detect(self, frame_rgb):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        return self.detector.detect(mp_image)

class GestureProcessor:
    def __init__(self):
        self.prev_hand_pos = None
        self.screen_width, self.screen_height = pyautogui.size()
        self.mouse_sensitivity = DEFAULT_SENSITIVITY
        pyautogui.FAILSAFE = False
    
    def process_gestures(self, hand_measurements):
        if not hand_measurements:
            return
            
        hand = hand_measurements[0]
        if hand['distance'] < 40:
            self._update_mouse_position(hand['index_finger'], hand['hand_size'])
        else:
            self.prev_hand_pos = None
        
        if hand['middle_distance'] < 30:
            pyautogui.click()

    def _update_mouse_position(self, current_pos, hand_size):
        if self.prev_hand_pos is None:
            self.prev_hand_pos = current_pos
            return
        
        scale_factor = hand_size / REFERENCE_HAND_SIZE
        dx = -(current_pos[0] - self.prev_hand_pos[0]) * scale_factor
        dy = (current_pos[1] - self.prev_hand_pos[1]) * scale_factor
        
        current_x, current_y = pyautogui.position()
        new_x = current_x + dx * self.mouse_sensitivity
        new_y = current_y + dy * self.mouse_sensitivity
        
        new_x = max(0, min(new_x, self.screen_width))
        new_y = max(0, min(new_y, self.screen_height))
        
        pyautogui.moveTo(new_x, new_y)
        self.prev_hand_pos = current_pos

def draw_landmarks_on_image(rgb_image, detection_result):
    hand_landmarks_list = detection_result.hand_landmarks
    annotated_image = np.copy(rgb_image)
    hand_measurements = []
    height, width, _ = annotated_image.shape

    for idx, hand_landmarks in enumerate(hand_landmarks_list):
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=lm.x, y=lm.y, z=lm.z) for lm in hand_landmarks
        ])
        
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            hand_landmarks_proto,
            solutions.hands.HAND_CONNECTIONS,
            solutions.drawing_styles.get_default_hand_landmarks_style(),
            solutions.drawing_styles.get_default_hand_connections_style())

        # Landmarks clave
        wrist = hand_landmarks[0]
        thumb = hand_landmarks[4]
        index = hand_landmarks[8]
        middle = hand_landmarks[12]
        middle_mcp = hand_landmarks[9]

        # Conversión a coordenadas de píxeles
        thumb_x = int(thumb.x * width)
        thumb_y = int(thumb.y * height)
        index_x = int(index.x * width)
        index_y = int(index.y * height)
        middle_x = int(middle.x * width)
        middle_y = int(middle.y * height)
        wrist_x = int(wrist.x * width)
        wrist_y = int(wrist.y * height)
        middle_mcp_x = int(middle_mcp.x * width)
        middle_mcp_y = int(middle_mcp.y * height)

        # Cálculo del tamaño de la mano para escalado
        hand_size = np.hypot(wrist_x - middle_mcp_x, wrist_y - middle_mcp_y)
        
        # Distancia pulgar-índice
        index_thumb_distance = np.hypot(thumb_x - index_x, thumb_y - index_y)
        
        # Distancia pulgar-medio (para click)
        middle_thumb_distance = np.hypot(thumb_x - middle_x, thumb_y - middle_y)

        # Dibujar línea y texto
        cv2.line(annotated_image, (thumb_x, thumb_y), (index_x, index_y), (0, 255, 0), 2)
        mid_x = (thumb_x + index_x) // 2
        mid_y = (thumb_y + index_y) // 2
        cv2.putText(annotated_image, f"{int(index_thumb_distance)}px", 
                   (mid_x, mid_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        hand_measurements.append({
            'distance': int(index_thumb_distance),
            'index_finger': (index_x, index_y),
            'hand_size': hand_size,
            'middle_distance': int(middle_thumb_distance)
        })

    return annotated_image, hand_measurements
