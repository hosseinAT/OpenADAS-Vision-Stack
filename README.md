# OpenADAS Vision Stack

Ein modularer, eigenständig aufgebauter ADAS-Demonstrator für kamerabasierte Umfeldwahrnehmung und Sicherheitsbewertung.

## Funktionen

- klassische Fahrspurerkennung mit OpenCV
- Fahrbahnmitte und Spurabweichung
- einfache Objektverfolgung über Bounding-Box-Zentren
- monokulare Distanzschätzung über konfigurierbare Objektbreiten
- Time-to-Collision
- Risikobewertung: SAFE, CAUTION, WARNING, CRITICAL
- kombinierte Dashboard-Visualisierung
- Video-, Bild- und Kameraeingabe
- automatisierte Tests
- Dockerfile und GitHub Actions

## Wichtiger Hinweis

Dieses Repository ist ein eigenständiger Lern- und Portfolio-Demonstrator. Die Baseline verwendet OpenCV und simulierte bzw. manuell übergebene Objektdetektionen. Deep-Learning, ONNX, TensorRT, ROS2 und Jetson-Tests sind als Erweiterungen vorgesehen, aber im aktuellen Stand noch nicht vollständig integriert.

## Installation unter Windows

```powershell
py -m venv .venv
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest
```

## Schnellstart

```powershell
python -m examples.demo_image
```

Video:

```powershell
python -m examples.run_video --input input.mp4 --output output.mp4
```

## Interview-Erklärung

> I developed a modular ADAS vision pipeline in Python and OpenCV. The system detects lane boundaries, estimates the vehicle offset from the lane center, tracks detected objects, estimates object distance, calculates time-to-collision, and assigns safety states. I also added tests and a modular architecture so that deep-learning, ROS2, and TensorRT components can be integrated later.

## Lizenz

MIT
