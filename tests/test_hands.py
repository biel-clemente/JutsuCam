from types import SimpleNamespace

import numpy as np
import pytest

from jutsucam.hands.detector import ensure_model
from jutsucam.hands.drawing import draw_landmarks


def test_draw_landmarks_pinta_en_el_frame():
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    hand = [SimpleNamespace(x=0.5, y=0.5)] * 21
    draw_landmarks(frame, hand)
    assert frame[50, 50].any()


def test_ensure_model_descarga_sin_dejar_parciales(tmp_path):
    src = tmp_path / "origen.task"
    src.write_bytes(b"modelo")
    dest = tmp_path / "models" / "hand.task"

    ensure_model(dest, src.as_uri())

    assert dest.read_bytes() == b"modelo"
    assert not dest.with_suffix(".part").exists()


def test_ensure_model_limpia_si_la_descarga_falla(tmp_path):
    dest = tmp_path / "models" / "hand.task"
    url = (tmp_path / "no-existe.task").as_uri()

    with pytest.raises(RuntimeError, match="conexión"):
        ensure_model(dest, url)

    assert not dest.exists()
    assert not dest.with_suffix(".part").exists()
