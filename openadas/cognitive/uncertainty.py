from __future__ import annotations

from statistics import pstdev
from .types import Observation


class UncertaintyEstimator:
    """Rule-based uncertainty baseline.

    This baseline intentionally exposes every contributing factor so it can be
    replaced later by calibrated probabilistic or ensemble methods.
    """

    def estimate(self, obs: Observation) -> tuple[str, float, list[str]]:
        score = 0.0
        reasons: list[str] = []

        conf = min(max(float(obs.confidence), 0.0), 1.0)
        score += (1.0 - conf) * 0.35
        if conf < 0.50:
            reasons.append("low_detection_confidence")

        history = obs.class_history or [obs.class_name]
        if len(history) >= 2:
            switches = sum(a != b for a, b in zip(history[:-1], history[1:]))
            switch_rate = switches / (len(history) - 1)
            score += min(switch_rate, 1.0) * 0.30
            if switch_rate > 0.25:
                reasons.append("class_instability")

        conf_hist = obs.confidence_history or [conf]
        if len(conf_hist) >= 2:
            variation = min(pstdev(conf_hist), 0.5) / 0.5
            score += variation * 0.20
            if variation > 0.30:
                reasons.append("confidence_variation")

        sensor_health = min(max(float(obs.sensor_health), 0.0), 1.0)
        score += (1.0 - sensor_health) * 0.15
        if sensor_health < 0.70:
            reasons.append("degraded_sensor_health")

        score = min(max(score, 0.0), 1.0)
        if score < 0.30:
            level = "LOW"
        elif score < 0.60:
            level = "MEDIUM"
        else:
            level = "HIGH"

        return level, score, reasons
