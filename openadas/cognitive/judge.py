from __future__ import annotations

from collections import defaultdict
from .types import Evidence


class MultiModelJudge:
    """Weighted evidence fusion baseline for semantic decisions.

    This is deliberately transparent: every source contributes confidence x
    trust. It can later be replaced by Bayesian fusion, Dempster-Shafer,
    learned fusion, or calibrated ensembles.
    """

    def decide(self, evidences: list[Evidence]) -> dict:
        if not evidences:
            return {
                "label": "unknown_object",
                "confidence": 0.0,
                "agreement": 0.0,
                "evidence_count": 0,
            }

        support = defaultdict(float)
        count = defaultdict(int)
        total = 0.0
        for ev in evidences:
            w = ev.weighted_support
            support[ev.label] += w
            count[ev.label] += 1
            total += w

        best_label = max(support, key=support.get)
        confidence = support[best_label] / total if total > 0 else 0.0
        agreement = count[best_label] / len(evidences)

        return {
            "label": best_label,
            "confidence": confidence,
            "agreement": agreement,
            "evidence_count": len(evidences),
            "support": dict(support),
        }
