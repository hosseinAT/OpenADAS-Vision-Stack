from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelEvaluation:
    old_class_recall_delta: float
    new_class_recall_delta: float
    calibration_error: float
    latency_ms: float
    shadow_agreement: float
    critical_regressions: int = 0


class ModelLifecycleGate:
    """Transparent candidate promotion gate.

    A candidate is promoted only when every configured safety/quality gate
    passes. Thresholds are demonstrator defaults, not production certification.
    """

    def __init__(
        self,
        max_old_class_recall_drop: float = 0.01,
        min_new_class_recall_gain: float = 0.0,
        max_calibration_error: float = 0.08,
        max_latency_ms: float = 80.0,
        min_shadow_agreement: float = 0.90,
    ) -> None:
        self.max_old_class_recall_drop = max_old_class_recall_drop
        self.min_new_class_recall_gain = min_new_class_recall_gain
        self.max_calibration_error = max_calibration_error
        self.max_latency_ms = max_latency_ms
        self.min_shadow_agreement = min_shadow_agreement

    def evaluate(self, metrics: ModelEvaluation) -> dict:
        checks = {
            "old_class_regression": metrics.old_class_recall_delta >= -self.max_old_class_recall_drop,
            "new_class_gain": metrics.new_class_recall_delta >= self.min_new_class_recall_gain,
            "calibration": metrics.calibration_error <= self.max_calibration_error,
            "latency": metrics.latency_ms <= self.max_latency_ms,
            "shadow_agreement": metrics.shadow_agreement >= self.min_shadow_agreement,
            "critical_regressions": metrics.critical_regressions == 0,
        }
        failed = [name for name, ok in checks.items() if not ok]
        return {
            "promote": not failed,
            "failed_checks": failed,
            "checks": checks,
        }
