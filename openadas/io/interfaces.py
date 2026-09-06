from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional
import numpy as np

@dataclass
class CameraPacket:
    rgb: np.ndarray
    depth_m: Optional[np.ndarray]
    timestamp_s: float
    frame_id: int
    intrinsics: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class LidarObject:
    object_id: str
    xyz_m: tuple[float,float,float]
    extent_m: tuple[float,float,float]
    confidence: float = 1.0

@dataclass(frozen=True)
class RadarObject:
    object_id: str
    range_m: float
    radial_velocity_mps: float
    azimuth_rad: float
    confidence: float = 1.0
