"""Reconocimiento de gestos y sellos a partir de los landmarks de las manos."""

from jutsucam.seals.gestures import Gesture, recognize
from jutsucam.seals.stabilizer import GestureStabilizer

__all__ = ["Gesture", "GestureStabilizer", "recognize"]
