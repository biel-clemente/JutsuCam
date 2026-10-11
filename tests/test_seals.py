import json
from pathlib import Path
from types import SimpleNamespace as P

from jutsucam.seals import Gesture, GestureStabilizer, recognize
from jutsucam.seals.gestures import is_heart, is_thumbs_up

FIXTURES = Path(__file__).parent / "fixtures"

# Puño de lado con el pulgar estirado hacia arriba (coordenadas normalizadas, y hacia abajo).
THUMBS_UP = [
    P(x=0.50, y=0.70),  # 0 muñeca
    P(x=0.46, y=0.62),
    P(x=0.45, y=0.55),
    P(x=0.45, y=0.48),
    P(x=0.45, y=0.41),  # pulgar
    P(x=0.52, y=0.58),
    P(x=0.60, y=0.58),
    P(x=0.58, y=0.62),
    P(x=0.54, y=0.62),  # índice
    P(x=0.52, y=0.62),
    P(x=0.60, y=0.63),
    P(x=0.58, y=0.66),
    P(x=0.54, y=0.66),  # corazón
    P(x=0.52, y=0.66),
    P(x=0.59, y=0.67),
    P(x=0.57, y=0.70),
    P(x=0.54, y=0.70),  # anular
    P(x=0.52, y=0.69),
    P(x=0.58, y=0.71),
    P(x=0.56, y=0.73),
    P(x=0.54, y=0.73),  # meñique
]

# Mano abierta con los dedos hacia arriba.
OPEN_PALM = [
    P(x=0.50, y=0.80),
    P(x=0.42, y=0.74),
    P(x=0.38, y=0.68),
    P(x=0.35, y=0.62),
    P(x=0.33, y=0.57),
    P(x=0.45, y=0.62),
    P(x=0.44, y=0.52),
    P(x=0.44, y=0.46),
    P(x=0.44, y=0.41),
    P(x=0.50, y=0.61),
    P(x=0.50, y=0.50),
    P(x=0.50, y=0.44),
    P(x=0.50, y=0.38),
    P(x=0.55, y=0.62),
    P(x=0.56, y=0.52),
    P(x=0.56, y=0.46),
    P(x=0.56, y=0.42),
    P(x=0.59, y=0.65),
    P(x=0.61, y=0.57),
    P(x=0.62, y=0.52),
    P(x=0.63, y=0.48),
]


def mirror_y(hand):
    return [P(x=p.x, y=1 - p.y) for p in hand]


def heart_hand(side, index_tip, thumb_tip, index_curled):
    """Mano de un corazón a dos manos. side=-1 izquierda, +1 derecha."""
    cx = 0.5 + side * 0.15
    hand = [P(x=cx, y=0.6) for _ in range(21)]
    hand[0] = P(x=cx, y=0.65)  # muñeca
    hand[9] = P(x=cx - side * 0.03, y=0.50)  # nudillo del dedo corazón -> tamaño ~0,15
    hand[4] = P(x=thumb_tip, y=0.62)
    hand[8] = P(x=index_tip, y=0.40)
    hand[6] = P(x=index_tip, y=0.36 if index_curled else 0.45)  # nudillo medio del índice
    return hand


def heart(gap=0.02, index_curled=True):
    left = heart_hand(-1, 0.5 - gap / 2, 0.5 - gap / 2, index_curled)
    right = heart_hand(+1, 0.5 + gap / 2, 0.5 + gap / 2, index_curled)
    return [left, right]


def test_pulgar_arriba():
    assert is_thumbs_up(THUMBS_UP)
    assert recognize([THUMBS_UP]) is Gesture.THUMBS_UP


def test_pulgar_abajo_no_es_pulgar_arriba():
    assert not is_thumbs_up(mirror_y(THUMBS_UP))


def test_mano_abierta_no_es_pulgar_arriba():
    assert not is_thumbs_up(OPEN_PALM)
    assert recognize([OPEN_PALM]) is None


def test_corazon_con_dos_manos():
    assert is_heart(*heart())
    assert recognize(heart()) is Gesture.HEART


def test_manos_separadas_no_son_corazon():
    assert not is_heart(*heart(gap=0.3))


def test_manos_rezando_no_son_corazon():
    # Rezando, los índices van estirados: la punta queda por encima del nudillo.
    assert not is_heart(*heart(index_curled=False))


def test_sin_manos_no_hay_gesto():
    assert recognize([]) is None


def test_estabilizador_confirma_tras_n_frames():
    s = GestureStabilizer(frames=3)
    assert s.update(Gesture.HEART) is None
    assert s.update(Gesture.HEART) is None
    assert s.update(Gesture.HEART) is Gesture.HEART


def test_estabilizador_ignora_parpadeos():
    s = GestureStabilizer(frames=3)
    for _ in range(3):
        s.update(Gesture.HEART)
    assert s.update(None) is Gesture.HEART  # un frame suelto no lo quita
    assert s.update(Gesture.HEART) is Gesture.HEART


def test_corazon_real_capturado_con_la_camara():
    data = json.loads((FIXTURES / "heart_real.json").read_text(encoding="utf-8"))
    hands = [[P(**p) for p in hand] for hand in data]
    assert recognize(hands) is Gesture.HEART
