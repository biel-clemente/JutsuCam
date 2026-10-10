"""Detección de manos con MediaPipe Hand Landmarker (API Tasks)."""

import shutil
import time
import urllib.request

import cv2
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions, vision

from jutsucam.config import MAX_HANDS, MODEL_DOWNLOAD_TIMEOUT_S, MODEL_PATH, MODEL_URL


def ensure_model(path=MODEL_PATH, url=MODEL_URL):
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    print("Descargando modelo de detección de manos...")
    tmp = path.with_suffix(".part")
    try:
        with (
            urllib.request.urlopen(url, timeout=MODEL_DOWNLOAD_TIMEOUT_S) as resp,
            open(tmp, "wb") as f,
        ):
            shutil.copyfileobj(resp, f)
        tmp.replace(path)  # solo se renombra si la descarga terminó entera
    except OSError as e:  # URLError, timeout, disco lleno...
        raise RuntimeError(
            f"No se pudo descargar el modelo de manos desde {url}. Revisa tu conexión a internet."
        ) from e
    finally:
        tmp.unlink(missing_ok=True)


class HandDetector:
    """Envuelve HandLandmarker en modo vídeo. Úsalo con `with`."""

    def __init__(self, model_path=MODEL_PATH, num_hands=MAX_HANDS):
        ensure_model(model_path)
        options = vision.HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(model_path)),
            running_mode=vision.RunningMode.VIDEO,
            num_hands=num_hands,
        )
        self._landmarker = vision.HandLandmarker.create_from_options(options)
        self._start = time.monotonic()
        self._last_ts = -1

    def detect(self, frame_bgr):
        """Devuelve una lista de manos; cada mano son 21 landmarks con x, y normalizados."""
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        # MediaPipe exige timestamps estrictamente crecientes
        ts = max(int((time.monotonic() - self._start) * 1000), self._last_ts + 1)
        self._last_ts = ts
        return self._landmarker.detect_for_video(image, ts).hand_landmarks

    def close(self):
        self._landmarker.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
