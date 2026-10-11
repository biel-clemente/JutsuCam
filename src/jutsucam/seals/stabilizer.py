"""Filtro temporal: un gesto cuenta si aparece en la mayoría de los últimos frames."""

from collections import Counter, deque

from jutsucam.config import GESTURE_MIN_HITS, GESTURE_WINDOW_FRAMES


class GestureStabilizer:
    # Ventana con mayoría en vez de N frames seguidos: con las manos juntas MediaPipe falla
    # en frames sueltos, y eso no debe reiniciar la cuenta.
    def __init__(self, window=GESTURE_WINDOW_FRAMES, min_hits=GESTURE_MIN_HITS):
        self.min_hits = min_hits
        self.current = None
        self._recent = deque(maxlen=window)

    def update(self, gesture):
        """Recibe el gesto del frame actual y devuelve el gesto confirmado (o None)."""
        self._recent.append(gesture)
        candidate, hits = Counter(self._recent).most_common(1)[0]
        # Funciona en los dos sentidos: "sin gesto" también necesita mayoría para quitarlo.
        if hits >= self.min_hits:
            self.current = candidate
        return self.current
