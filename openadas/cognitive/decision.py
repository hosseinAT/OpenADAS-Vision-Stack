from __future__ import annotations

from .types import Decision, Observation


class SafetyDecisionManager:
    """Transparent advisory risk logic for the research demonstrator.

    The output is intentionally advisory only. It must not be connected to a
    real road vehicle actuation stack without a separate safety architecture,
    validation plan and certified control layer.
    """

    def decide(self, obs: Observation, uncertainty_score: float) -> Decision:
        distance = obs.distance_m if obs.distance_m is not None else float("inf")
        sensor_penalty = 1.0 - min(max(obs.sensor_health, 0.0), 1.0)
        approach_penalty = 0.25 if obs.approaching else 0.0
        distance_penalty = 0.0

        if distance < 2.5:
            distance_penalty = 0.55
        elif distance < 4.0:
            distance_penalty = 0.40
        elif distance < 8.0:
            distance_penalty = 0.20

        score = min(
            1.0,
            0.45 * uncertainty_score
            + distance_penalty
            + approach_penalty
            + 0.20 * sensor_penalty,
        )

        if score >= 0.80:
            action, risk = "STOP_REQUEST", "CRITICAL"
        elif score >= 0.60:
            action, risk = "PREPARE_TO_STOP", "HIGH"
        elif score >= 0.35:
            action, risk = "SLOW_DOWN", "MEDIUM"
        else:
            action, risk = "CONTINUE", "LOW"

        reason = (
            f"distance_m={distance:.2f}, approaching={obs.approaching}, "
            f"uncertainty={uncertainty_score:.2f}, sensor_health={obs.sensor_health:.2f}"
        )
        return Decision(action=action, risk=risk, reason=reason, score=score)
