from __future__ import annotations
from dataclasses import dataclass
from openadas.cognitive.types import Evidence

@dataclass(frozen=True)
class TrustContext:
    camera_health: float = 1.0
    lidar_health: float = 1.0
    radar_health: float = 1.0
    memory_similarity: float = 0.0

def sensor_trust(base: float, health: float) -> float:
    return max(0.0,min(1.0,float(base)*max(0.0,min(1.0,float(health)))))

def build_evidence(source:str,label:str,confidence:float,base_trust:float=1.0,health:float=1.0,**metadata)->Evidence:
    return Evidence(source=source,label=label,confidence=float(confidence),trust=sensor_trust(base_trust,health),metadata=metadata)

def memory_evidence(label:str, similarity:float, min_similarity:float=0.70)->Evidence|None:
    sim=max(0.0,min(1.0,float(similarity)))
    if sim < min_similarity: return None
    return Evidence(source='episodic_memory',label=label,confidence=sim,trust=min(0.85,sim),metadata={'similarity':sim})
