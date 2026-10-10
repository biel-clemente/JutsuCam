# JutsuCam

Haz sellos de mano ninja delante de la webcam y lanza jutsus en tiempo real: para tus videollamadas (Google Meet), para OBS o para tus grabaciones.

> Estado: en desarrollo. Ahora mismo detecta las manos por la cámara. Los primeros jutsus (convertirse en madera y multiplicarse) llegarán después.

## Requisitos

- Python 3.10+
- Una webcam

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -e .
```

## Uso

```bash
python -m jutsucam
```

La primera vez descarga el modelo de detección de manos de MediaPipe (~8 MB) en `%LOCALAPPDATA%\jutsucam`. Para salir, pulsa `q`, `Esc` o cierra la ventana.

**Windows:** si la cámara no abre, activa *Configuración → Privacidad y seguridad → Cámara → Permitir que las aplicaciones de escritorio accedan a tu cámara*.

## Tecnología

- [OpenCV](https://opencv.org/) para la captura de vídeo
- [MediaPipe Hand Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker) para detectar las manos

## Desarrollo

```bash
pip install -e ".[dev]"
python -m pytest
python -m ruff check . && python -m ruff format --check .
```

La estructura del código se explica en [`docs/architecture.md`](docs/architecture.md) y las decisiones técnicas en [`docs/decisions/`](docs/decisions/).
