# Arquitectura

## Estructura

```
JutsuCam/
├── src/jutsucam/          # código de la app (paquete instalable)
│   ├── app.py             # bucle principal: cámara -> detección -> render
│   ├── camera.py          # apertura de la webcam (backends Windows)
│   ├── config.py          # constantes: caché, modelo, teclas, ventana
│   └── hands/             # todo lo relativo a las manos
│       ├── detector.py    # HandDetector (MediaPipe Hand Landmarker)
│       └── drawing.py     # dibujo de los 21 puntos de la mano
├── tests/                 # pytest, un archivo por módulo
├── docs/
│   ├── architecture.md    # este archivo
│   └── decisions/         # ADRs: una decisión técnica por archivo
└── pyproject.toml         # dependencias, scripts, config de pytest y ruff
```

## Flujo por frame

1. `camera` abre la webcam y `app` lee cada frame BGR y lo espeja con `cv2.flip`.
2. `hands.HandDetector.detect` devuelve las manos (21 landmarks cada una, en coordenadas 0-1).
3. `hands.draw_landmarks` las pinta y `app` muestra el resultado. Se sale con `q`, `Esc` o cerrando la ventana.

## Cómo crecerá

Cada funcionalidad nueva va en su propio subpaquete, que se crea cuando se implemente:

- `seals/`: reconocer un sello de mano a partir de los landmarks (lógica pura y testeable, sin cámara).
- `jutsus/`: un módulo por jutsu (`clones.py`, `madera.py`...). Cada uno recibe el frame y devuelve el frame con el efecto aplicado.
- `output/`: cámara virtual para Meet/OBS (p. ej. `pyvirtualcam`).

Reglas:
- Las dependencias van en una sola dirección: `app` -> `jutsus` -> `seals` -> `hands`. Nada importa `app`.
- La lógica sin E/S (reconocer sellos, geometría) no toca cámara ni ventanas, así se puede testear.
