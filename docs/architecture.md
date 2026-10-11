# Arquitectura

## Estructura

```
JutsuCam/
├── src/jutsucam/          # código de la app (paquete instalable)
│   ├── app.py             # bucle principal: cámara -> detección -> render
│   ├── camera.py          # apertura de la webcam (backends Windows)
│   ├── config.py          # constantes: caché, modelo, teclas, ventana
│   ├── hands/             # todo lo relativo a las manos
│   │   ├── detector.py    # HandDetector (MediaPipe Hand Landmarker)
│   │   └── drawing.py     # dibujo de los 21 puntos de la mano
│   └── seals/             # reconocimiento de gestos y sellos (geometría pura, sin cámara)
│       ├── gestures.py    # Gesture + reglas: corazón, pulgar arriba
│       └── stabilizer.py  # un gesto solo cuenta si se mantiene N frames
├── tests/                 # pytest, un archivo por módulo
├── docs/
│   ├── architecture.md    # este archivo
│   └── decisions/         # ADRs: una decisión técnica por archivo
└── pyproject.toml         # dependencias, scripts, config de pytest y ruff
```

## Flujo por frame

1. `camera` abre la webcam y `app` lee cada frame BGR y lo espeja con `cv2.flip`.
2. `hands.HandDetector.detect` devuelve las manos (21 landmarks cada una, en coordenadas 0-1).
3. `hands.draw_landmarks` las pinta.
4. `seals.recognize` decide qué gesto forman y `GestureStabilizer` lo confirma si se mantiene
   `GESTURE_STABLE_FRAMES` frames seguidos.
5. `app` escribe el nombre del gesto y muestra el resultado. Se sale con `q`, `Esc` o cerrando la ventana.

## Cómo crecerá

Cada funcionalidad nueva va en su propio subpaquete, que se crea cuando se implemente:

- `jutsus/`: un módulo por jutsu (`clones.py`, `madera.py`...). Cada uno recibe el frame y devuelve el frame con el efecto aplicado.
- `output/`: cámara virtual para Meet/OBS (p. ej. `pyvirtualcam`).

Reglas:
- Las dependencias van en una sola dirección: `app` -> `jutsus` -> `seals` -> `hands`. Nada importa `app`.
- La lógica sin E/S (reconocer sellos, geometría) no toca cámara ni ventanas, así se puede testear.
