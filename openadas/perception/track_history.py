from __future__ import annotations
from collections import deque, Counter
from dataclasses import dataclass, field

@dataclass
class TrackHistory:
    maxlen: int = 60
    classes: deque[str] = field(init=False)
    confidences: deque[float] = field(init=False)
    distances_m: deque[float] = field(init=False)
    def __post_init__(self):
        self.classes=deque(maxlen=self.maxlen); self.confidences=deque(maxlen=self.maxlen); self.distances_m=deque(maxlen=self.maxlen)
    def add(self,class_name:str,confidence:float,distance_m:float|None=None)->None:
        self.classes.append(class_name); self.confidences.append(float(confidence))
        if distance_m is not None: self.distances_m.append(float(distance_m))
    @property
    def frames(self)->int: return len(self.classes)
    @property
    def dominant_class(self)->str: return Counter(self.classes).most_common(1)[0][0] if self.classes else 'unknown_object'
    @property
    def temporal_consistency(self)->float:
        if not self.classes: return 0.0
        c=Counter(self.classes); return c[self.dominant_class]/len(self.classes)
    @property
    def approaching(self)->bool:
        if len(self.distances_m)<3: return False
        d=list(self.distances_m)[-min(5,len(self.distances_m)):]; return d[-1] < d[0]-0.15

class TrackHistoryStore:
    def __init__(self,maxlen:int=60): self.maxlen=maxlen; self._tracks={}
    def update(self,track_id:int,class_name:str,confidence:float,distance_m:float|None=None)->TrackHistory:
        hist=self._tracks.setdefault(int(track_id),TrackHistory(self.maxlen)); hist.add(class_name,confidence,distance_m); return hist
    def get(self,track_id:int)->TrackHistory|None: return self._tracks.get(int(track_id))
