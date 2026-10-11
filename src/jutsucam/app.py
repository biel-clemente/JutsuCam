"""Bucle principal: cámara -> detección de manos -> gestos -> render."""

import sys

import cv2

from jutsucam.camera import open_camera
from jutsucam.config import QUIT_KEYS, WINDOW_NAME
from jutsucam.hands import HandDetector, draw_landmarks
from jutsucam.seals import GestureStabilizer, recognize


def _window_closed():
    return cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1


def _draw_label(frame, text):
    for color, thickness in (((0, 0, 0), 6), ((255, 255, 255), 2)):  # contorno + texto
        cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, thickness)


def run():
    stabilizer = GestureStabilizer()
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
                hands = detector.detect(frame)
                for hand in hands:
                    draw_landmarks(frame, hand)

                gesture = stabilizer.update(recognize(hands))
                if gesture:
                    _draw_label(frame, gesture.value)

                cv2.imshow(WINDOW_NAME, frame)
                if cv2.waitKey(1) & 0xFF in QUIT_KEYS or _window_closed():
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()
