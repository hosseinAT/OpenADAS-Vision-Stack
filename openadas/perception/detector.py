from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Detection:
    bbox_xyxy: tuple[int,int,int,int]
    class_name: str
    confidence: float
    class_id: int | None = None

class YoloDetector:
    """Optional Ultralytics adapter; core package remains dependency-light."""
    def __init__(self, model_path:str='yolo11n.pt', conf:float=0.25, device:str|None=None):
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise RuntimeError("Install optional dependency: pip install -e '.[vision]'") from exc
        self.model=YOLO(model_path); self.conf=conf; self.device=device
    def predict(self, image) -> list[Detection]:
        results=self.model.predict(image,conf=self.conf,device=self.device,verbose=False); out=[]
        for r in results:
            if r.boxes is None: continue
            for box in r.boxes:
                xyxy=box.xyxy[0].tolist(); cid=int(box.cls[0]); conf=float(box.conf[0])
                out.append(Detection(tuple(int(round(v)) for v in xyxy),str(r.names[cid]),conf,cid))
        return out
