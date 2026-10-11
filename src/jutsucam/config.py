"""Constantes de configuración de la app."""

import os
from pathlib import Path

# Caché por usuario: funciona igual con instalación editable o normal, sin escribir en el Python.
CACHE_DIR = Path(os.environ.get("LOCALAPPDATA") or Path.home() / ".cache") / "jutsucam"

MODEL_PATH = CACHE_DIR / "models" / "hand_landmarker.task"
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/latest/hand_landmarker.task"
)
MODEL_DOWNLOAD_TIMEOUT_S = 60
MAX_HANDS = 2
# Por defecto MediaPipe usa 0,5; con las manos pegadas (p. ej. el corazón) pierde una.
HAND_MIN_CONFIDENCE = 0.3
GESTURE_STABLE_FRAMES = 8  # ~0,25 s a 30 fps

WINDOW_NAME = "JutsuCam"
QUIT_KEYS = (27, ord("q"))  # Esc, q
