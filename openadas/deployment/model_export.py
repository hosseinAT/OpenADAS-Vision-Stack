from __future__ import annotations
from pathlib import Path

def export_ultralytics_onnx(model_path:str,imgsz:int=640,half:bool=False,dynamic:bool=True)->Path:
    try: from ultralytics import YOLO
    except ImportError as exc: raise RuntimeError("Install vision dependencies first: pip install -e '.[vision]'") from exc
    return Path(str(YOLO(model_path).export(format='onnx',imgsz=imgsz,half=half,dynamic=dynamic,simplify=True)))

def export_ultralytics_tensorrt(model_path:str,imgsz:int=640,half:bool=True,device:int=0)->Path:
    try: from ultralytics import YOLO
    except ImportError as exc: raise RuntimeError("Install vision dependencies first: pip install -e '.[vision]'") from exc
    return Path(str(YOLO(model_path).export(format='engine',imgsz=imgsz,half=half,device=device)))
