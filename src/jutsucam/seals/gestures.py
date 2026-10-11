"""Gestos reconocidos por geometría sobre los 21 landmarks de MediaPipe.

Índices: 0 muñeca; pulgar 1-4; índice 5-8; corazón 9-12; anular 13-16; meñique 17-20.
Coordenadas normalizadas (0-1), con la y creciendo hacia abajo.
Los umbrales son relativos al tamaño de la mano (muñeca -> nudillo del dedo corazón),
así que no dependen de lo cerca que estés de la cámara.
"""

import math
from enum import Enum

WRIST, THUMB_MCP, THUMB_IP, THUMB_TIP = 0, 2, 3, 4
INDEX_PIP, INDEX_TIP, MIDDLE_MCP, MIDDLE_PIP, MIDDLE_TIP = 6, 8, 9, 10, 12
RING_PIP, RING_TIP, PINKY_PIP, PINKY_TIP = 14, 16, 18, 20
# (punta, articulación media) de índice, corazón, anular y meñique
FINGERS = ((8, 6), (12, 10), (16, 14), (20, 18))

# Umbrales de calibración, relativos al tamaño de la mano: ajústalos probando en vivo.
THUMB_MIN_LENGTH = 0.5  # cuánto tiene que subir el pulgar por encima de su nudillo
HEART_MAX_GAP = 0.5  # distancia máxima entre las puntas que se tocan (índices y pulgares)
HEART_MIN_HEIGHT = 0.5  # altura mínima del corazón (de índices a pulgares)
TIGER_MIN_EXTENSION = 0.25  # cuánto sobresalen índice y corazón por encima de su nudillo
TIGER_MAX_FINGER_GAP = 0.35  # índice y corazón pegados (si no, es el signo de la victoria)


class Gesture(Enum):
    # Sin tildes: las fuentes de cv2.putText solo tienen caracteres ASCII.
    HEART = "Corazon"
    THUMBS_UP = "Pulgar arriba"
    TIGER = "Tigre"


def _dist(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def _hand_size(hand):
    return _dist(hand[WRIST], hand[MIDDLE_MCP])


def _fingers_folded(hand):
    wrist = hand[WRIST]
    return all(_dist(hand[tip], wrist) < _dist(hand[pip], wrist) for tip, pip in FINGERS)


def is_thumbs_up(hand):
    tip, ip, mcp = hand[THUMB_TIP], hand[THUMB_IP], hand[THUMB_MCP]
    rise = mcp.y - tip.y
    thumb_up = (
        tip.y < ip.y < mcp.y
        and rise > THUMB_MIN_LENGTH * _hand_size(hand)
        and abs(tip.x - mcp.x) < rise  # más vertical que horizontal
    )
    return thumb_up and _fingers_folded(hand)


def is_heart(hand_a, hand_b):
    size = (_hand_size(hand_a) + _hand_size(hand_b)) / 2
    index_a, index_b = hand_a[INDEX_TIP], hand_b[INDEX_TIP]
    thumb_a, thumb_b = hand_a[THUMB_TIP], hand_b[THUMB_TIP]
    top_y = (index_a.y + index_b.y) / 2
    bottom_y = (thumb_a.y + thumb_b.y) / 2
    return (
        _dist(index_a, index_b) < HEART_MAX_GAP * size
        and _dist(thumb_a, thumb_b) < HEART_MAX_GAP * size
        and bottom_y - top_y > HEART_MIN_HEIGHT * size
        # Índices curvados (punta por debajo del nudillo medio): así no se confunde con
        # las manos juntas rezando, donde la punta es lo más alto.
        and all(hand[INDEX_TIP].y > hand[INDEX_PIP].y for hand in (hand_a, hand_b))
    )


def _rise(hand, tip, pip):
    """Cuánto sube la punta del dedo por encima de su nudillo medio, relativo a la mano."""
    return (hand[pip].y - hand[tip].y) / _hand_size(hand)


def is_tiger_hand(hand):
    """Sello del Tigre visto en una mano: índice y corazón juntos hacia arriba, el resto doblados.

    Basta con una mano porque, con los dedos entrelazados, MediaPipe suele perder la de detrás.
    """
    return (
        _rise(hand, INDEX_TIP, INDEX_PIP) > TIGER_MIN_EXTENSION
        and _rise(hand, MIDDLE_TIP, MIDDLE_PIP) > TIGER_MIN_EXTENSION
        and _rise(hand, RING_TIP, RING_PIP) < 0
        and _rise(hand, PINKY_TIP, PINKY_PIP) < 0
        and _dist(hand[INDEX_TIP], hand[MIDDLE_TIP]) < TIGER_MAX_FINGER_GAP * _hand_size(hand)
    )


def recognize(hands):
    """Devuelve el Gesture que forman las manos detectadas, o None."""
    if len(hands) == 2 and is_heart(*hands):
        return Gesture.HEART
    if any(is_tiger_hand(hand) for hand in hands):
        return Gesture.TIGER
    if any(is_thumbs_up(hand) for hand in hands):
        return Gesture.THUMBS_UP
    return None
