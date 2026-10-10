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
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

La primera vez descarga el modelo de detección de manos de MediaPipe en `models/`. Para salir, pulsa `q` o `Esc`.

**Windows:** si la cámara no abre, activa *Configuración → Privacidad y seguridad → Cámara → Permitir que las aplicaciones de escritorio accedan a tu cámara*.

## Tecnología

- [OpenCV](https://opencv.org/) para la captura de vídeo
- [MediaPipe Hand Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker) para detectar las manos
