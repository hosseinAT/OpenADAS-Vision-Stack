from __future__ import annotations
import math
from .track_history import TrackHistory

def compact_episode_embedding(class_name:str, confidence:float, distance_m:float|None, sensor_health:float, history:TrackHistory|None=None)->tuple[float,...]:
    semantic=(sum(ord(c) for c in class_name)%997)/997.0
    dist=1.0/(1.0+max(float(distance_m or 100.0),0.0)); consistency=history.temporal_consistency if history else 0.0
    approach=1.0 if history and history.approaching else 0.0; frames=min((history.frames if history else 0)/60.0,1.0)
    vec=[semantic,float(confidence),dist,float(sensor_health),consistency,approach,frames]
    norm=math.sqrt(sum(v*v for v in vec)) or 1.0
    return tuple(v/norm for v in vec)
