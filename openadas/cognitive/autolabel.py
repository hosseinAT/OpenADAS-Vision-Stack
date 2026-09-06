from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AutoLabelResult:
    accepted: bool
    label: str
    confidence: float
    reason: str


class AutoLabelGate:
    """Conservative pseudo-label gate for autonomous dataset growth."""

    def __init__(
        self,
        min_track_frames: int = 30,
        min_confidence: float = 0.85,
        min_temporal_consistency: float = 0.90,
        min_model_agreement: float = 0.80,
    ) -> None:
        self.min_track_frames = min_track_frames
        self.min_confidence = min_confidence
        self.min_temporal_consistency = min_temporal_consistency
        self.min_model_agreement = min_model_agreement

    def evaluate(
        self,
        proposed_label: str,
        confidence: float,
        track_frames: int,
        temporal_consistency: float,
        model_agreement: float,
        safe_fallback_label: str = "unknown_object",
    ) -> AutoLabelResult:
        checks = {
            "track_length": track_frames >= self.min_track_frames,
            "confidence": confidence >= self.min_confidence,
            "temporal_consistency": temporal_consistency >= self.min_temporal_consistency,
            "model_agreement": model_agreement >= self.min_model_agreement,
        }
        failed = [name for name, passed in checks.items() if not passed]

        if failed:
            return AutoLabelResult(
                accepted=False,
                label=safe_fallback_label,
                confidence=confidence,
                reason="failed:" + ",".join(failed),
            )

        return AutoLabelResult(
            accepted=True,
            label=proposed_label,
            confidence=confidence,
            reason="all_auto_label_gates_passed",
        )
