"""Filtro temporal: un gesto solo cuenta si se mantiene varios frames seguidos."""

from jutsucam.config import GESTURE_STABLE_FRAMES


class GestureStabilizer:
    def __init__(self, frames=GESTURE_STABLE_FRAMES):
        self.frames = frames
        self.current = None
        self._candidate = None
        self._count = 0

    def update(self, gesture):
        """Recibe el gesto del frame actual y devuelve el gesto confirmado (o None)."""
        if gesture == self._candidate:
            self._count += 1
        else:
            self._candidate, self._count = gesture, 1
        # Funciona en los dos sentidos: también hacen falta N frames para dejar de verlo.
        if self._count >= self.frames:
            self.current = gesture
        return self.current
