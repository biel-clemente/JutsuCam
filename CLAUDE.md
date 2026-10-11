# JutsuCam

Sellos de mano ninja ante la webcam para lanzar jutsus en tiempo real (Meet, OBS, grabaciones).
Python, OpenCV y MediaPipe. Repo: https://github.com/biel-clemente/JutsuCam

## Idioma
Responde en español. El código, los comentarios y los commits también van en español.

## Comandos (Windows, desde la raíz del repo)
- Ejecutar: `.venv\Scripts\python.exe -m jutsucam`
- Tests: `.venv\Scripts\python.exe -m pytest`
- Lint y formato: `.venv\Scripts\python.exe -m ruff check --fix . ; .venv\Scripts\python.exe -m ruff format .`
- Instalar (dev): `.venv\Scripts\python.exe -m pip install -e ".[dev]"`

## Arquitectura
Ver `docs/architecture.md`. Paquete en `src/jutsucam/`, un subpaquete por funcionalidad
(`hands/` ya existe; `seals/`, `jutsus/` y `output/` se crean cuando se implementen).
Las decisiones técnicas se apuntan como ADR en `docs/decisions/NNNN-titulo.md`.

## Reglas
- No uses "Naruto" como nombre, marca ni texto del producto (código, UI, README, assets), porque es
  una marca registrada. Solo puede aparecer en el ADR 0001, que explica por qué no se usa.
- MediaPipe: solo la API `mediapipe.tasks`, nunca `mp.solutions` (ver ADR 0002).
- El modelo se descarga en la caché del usuario (`%LOCALAPPDATA%\jutsucam`), nunca dentro del repo.
- Cada sello de mano nuevo lleva su test en `tests/`, con landmarks sintéticos (sin cámara).

## Fases
El proyecto avanza por fases, una cada vez. No adelantes trabajo de fases futuras.
Al cerrar una fase: tests en verde, commit + push y actualizar la sección "Fases del proyecto" en Notion
(qué se ha hecho, commits y estado de la siguiente fase). El plan de fases vive en Notion.

## Documentación del proyecto
La gestión del proyecto (ideas, estado, jutsus planeados) está en Notion, en la página
"JutsuCam" de CLEMENTE OS / PROYECTOS:
https://app.notion.com/p/3f5de8e6efd980658bcdd9cef44437c0
Actualízala con el conector de Notion. La documentación técnica va en `docs/`.

## Windows
Si la cámara no abre: Configuración > Privacidad y seguridad > Cámara >
"Permitir que las aplicaciones de escritorio accedan a tu cámara".
