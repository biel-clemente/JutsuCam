"""Apertura de la webcam."""

import cv2


def open_camera():
    # En Windows el backend MSMF por defecto a menudo falla al abrir la cámara;
    # DirectShow (CAP_DSHOW) es más fiable aquí.
    for backend in (cv2.CAP_DSHOW, cv2.CAP_ANY):
        for index in range(4):
            cap = cv2.VideoCapture(index, backend)
            if cap.isOpened():
                return cap
            cap.release()
    raise RuntimeError(
        "No se pudo abrir ninguna cámara (índices 0-3, backends DSHOW/por defecto). "
        "Revisa Configuración > Privacidad y seguridad > Cámara > "
        "'Permitir que las aplicaciones de escritorio accedan a tu cámara', "
        "y cierra otras apps que puedan estar usándola (Teams, Zoom, el navegador...)."
    )
