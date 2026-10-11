# 0003: Gestos reconocidos con reglas geométricas

- Fecha: 2026-10-10
- Estado: aceptada

**Contexto:** la fase 2 necesita reconocer el corazón (dos manos) y el pulgar arriba. Las fases siguientes necesitarán sellos ninja, muchos de ellos con las dos manos.

**Opciones:**
1. MediaPipe Gesture Recognizer: trae gestos fijos (pulgar arriba, puño, victoria...), pero no el corazón ni los sellos, y solo trabaja con una mano.
2. Entrenar un clasificador propio: exige grabar y etiquetar datos. Es excesivo para pocos gestos.
3. Reglas geométricas sobre los 21 landmarks que ya da Hand Landmarker.

**Decisión:** opción 3. Cada gesto es una función pura en `seals/gestures.py`, con umbrales relativos al tamaño de la mano y test con landmarks sintéticos. `GestureStabilizer` exige que el gesto se mantenga varios frames para evitar falsos positivos.

**Consecuencias:**
- No hay dependencias ni modelos nuevos, y todo es testeable sin cámara.
- Los umbrales (`THUMB_MIN_LENGTH`, `HEART_*`) se calibran probando en vivo.
- Si algún día hay decenas de sellos y las reglas no escalan, revisar la opción 2.

**Actualización (fase 3, sello del Tigre):** con los dedos entrelazados, MediaPipe pierde la mano de detrás en ~50 % de los frames. Por eso el Tigre se reconoce con **una sola mano** (índice y corazón juntos hacia arriba, anular y meñique doblados), que funciona tanto si se detectan 1 como 2 manos. Los umbrales se calibraron con una grabación real.
