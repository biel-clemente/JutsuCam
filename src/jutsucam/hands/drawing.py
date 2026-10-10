"""Dibujo de los landmarks de la mano sobre el frame."""

import cv2
from mediapipe.tasks.python import vision

CONNECTIONS = vision.HandLandmarksConnections.HAND_CONNECTIONS


def draw_landmarks(frame, hand_landmarks):
    h, w = frame.shape[:2]
    points = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks]
    for connection in CONNECTIONS:
        cv2.line(frame, points[connection.start], points[connection.end], (0, 255, 0), 2)
    for x, y in points:
        cv2.circle(frame, (x, y), 4, (0, 140, 255), -1)
