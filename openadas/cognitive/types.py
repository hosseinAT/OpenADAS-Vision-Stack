from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class Evidence:
    source: str
    label: str
    confidence: float
    trust: float = 1.0
    metadata: Dict[str, float | str | bool] = field(default_factory=dict)

    @property
    def weighted_support(self) -> float:
        confidence = min(max(float(self.confidence), 0.0), 1.0)
        trust = min(max(float(self.trust), 0.0), 1.0)
        return confidence * trust


@dataclass
class Observation:
    track_id: int
    class_name: str
    confidence: float
    distance_m: Optional[float] = None
    approaching: bool = False
    sensor_health: float = 1.0
    class_history: List[str] = field(default_factory=list)
    confidence_history: List[float] = field(default_factory=list)


@dataclass(frozen=True)
class Decision:
    action: str
    risk: str
    reason: str
    score: float


@dataclass
class Episode:
    episode_id: str
    embedding: Tuple[float, ...]
    semantic_label: str
    safety_label: str
    uncertainty: str
    action: str
    outcome: str = "UNKNOWN"
    metadata: Dict[str, str | float | int | bool] = field(default_factory=dict)
