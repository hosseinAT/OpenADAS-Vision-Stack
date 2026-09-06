from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class SensorHealth:
    score: float
    brightness: float
    blur_variance: float
    invalid_depth_ratio: float
    reasons: tuple[str,...]

def assess_camera_health(rgb: np.ndarray, depth_m: np.ndarray | None = None) -> SensorHealth:
    if rgb is None or rgb.size == 0:
        return SensorHealth(0.0,0.0,0.0,1.0,("empty_rgb",))
    gray = rgb.mean(axis=2) if rgb.ndim == 3 else rgb.astype(float)
    brightness = float(np.mean(gray))
    gx = np.diff(gray.astype(float), axis=1)
    gy = np.diff(gray.astype(float), axis=0)
    blur_variance = float(np.var(gx)) + float(np.var(gy))
    invalid_ratio = 0.0
    reasons=[]; penalty=0.0
    if brightness < 25:
        reasons.append('too_dark'); penalty += 0.25
    elif brightness > 235:
        reasons.append('overexposed'); penalty += 0.20
    if blur_variance < 20:
        reasons.append('low_texture_or_blur'); penalty += 0.20
    if depth_m is not None and depth_m.size:
        invalid = (~np.isfinite(depth_m)) | (depth_m <= 0)
        invalid_ratio = float(np.mean(invalid))
        if invalid_ratio > 0.30:
            reasons.append('degraded_depth'); penalty += min(0.35, invalid_ratio*0.5)
    score = max(0.0, min(1.0, 1.0-penalty))
    return SensorHealth(score, brightness, blur_variance, invalid_ratio, tuple(reasons))
