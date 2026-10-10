"""JutsuCam — base: webcam + hand landmark detection."""
import time
import urllib.request
from pathlib import Path

import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions

MODEL_PATH = Path("models/hand_landmarker.task")
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/latest/hand_landmarker.task"
)
CONNECTIONS = vision.HandLandmarksConnections.HAND_CONNECTIONS


def ensure_model():
    if not MODEL_PATH.exists():
        MODEL_PATH.parent.mkdir(exist_ok=True)
        print("Descargando modelo de detección de manos...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)


def draw_landmarks(frame, hand_landmarks):
    h, w = frame.shape[:2]
    points = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks]
    for connection in CONNECTIONS:
        cv2.line(frame, points[connection.start], points[connection.end], (0, 255, 0), 2)
    for x, y in points:
        cv2.circle(frame, (x, y), 4, (0, 140, 255), -1)


def open_camera():
    # En Windows el backend MSMF por defecto a menudo falla al abrir la cámara;
    # DirectShow (CAP_DSHOW) es más fiable aquí.
    for backend in (cv2.CAP_DSHOW, cv2.CAP_ANY):
        for index in range(4):
            cap = cv2.VideoCapture(index, backend)
            if cap.isOpened():
                return cap
            cap.release()
    raise RuntimeError(
        "No se pudo abrir ninguna cámara (índices 0-3, backends DSHOW/por defecto). "
        "Revisa Configuración > Privacidad y seguridad > Cámara > "
        "'Permitir que las aplicaciones de escritorio accedan a tu cámara', "
        "y cierra otras apps que puedan estar usándola (Teams, Zoom, el navegador...)."
    )


def main():
    ensure_model()

    options = vision.HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=str(MODEL_PATH)),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=2,
    )
    landmarker = vision.HandLandmarker.create_from_options(options)

    cap = open_camera()

    start_time = time.time()
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            timestamp_ms = int((time.time() - start_time) * 1000)
            result = landmarker.detect_for_video(mp_image, timestamp_ms)

            for hand_landmarks in result.hand_landmarks:
                draw_landmarks(frame, hand_landmarks)

            cv2.imshow("JutsuCam - manos", frame)
            if cv2.waitKey(1) & 0xFF in (27, ord("q")):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        landmarker.close()


if __name__ == "__main__":
    main()
