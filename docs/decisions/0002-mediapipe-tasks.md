# 0002: MediaPipe Tasks (Hand Landmarker) para detectar manos

- Fecha: 2026-10-10
- Estado: aceptada

**Contexto:** hace falta detectar en tiempo real los 21 puntos de cada mano con la webcam en un portátil sin GPU dedicada.

**Decisión:** MediaPipe Hand Landmarker con la API `mediapipe.tasks` en modo `VIDEO`. La API antigua `mp.solutions.hands` está obsoleta y no se usa.

**Consecuencias:**
- El modelo `.task` (~8 MB) se descarga la primera vez en la caché del usuario (`%LOCALAPPDATA%\jutsucam\models`), fuera del repo.
- El modo `VIDEO` exige timestamps estrictamente crecientes, así que `HandDetector` usa `time.monotonic()`.
