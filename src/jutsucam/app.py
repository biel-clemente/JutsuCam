"""Bucle principal: cámara -> detección de manos -> render."""

import sys

import cv2

from jutsucam.camera import open_camera
from jutsucam.config import QUIT_KEYS, WINDOW_NAME
from jutsucam.hands import HandDetector, draw_landmarks


def _window_closed():
    return cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1


def run():
    with HandDetector() as detector:
        cap = open_camera()
        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    sys.exit(
                        "La cámara dejó de enviar imagen. "
                        "¿La está usando otra app (Teams, Zoom, el navegador...)?"
                    )

                frame = cv2.flip(frame, 1)  # espejo, como un selfie
                for hand in detector.detect(frame):
                    draw_landmarks(frame, hand)

                cv2.imshow(WINDOW_NAME, frame)
                if cv2.waitKey(1) & 0xFF in QUIT_KEYS or _window_closed():
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()
