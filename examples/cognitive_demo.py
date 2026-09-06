"""Minimal end-to-end CognitiveDrive baseline demo.

Run:
    python -m examples.cognitive_demo

This demo uses synthetic evidence so the cognitive architecture can be tested
before RealSense/YOLO/LiDAR/radar integrations are added.
"""

from openadas.cognitive import (
    AutoLabelGate,
    EpisodicMemory,
    Evidence,
    MultiModelJudge,
    Observation,
    SafetyDecisionManager,
    UncertaintyEstimator,
)
from openadas.cognitive.types import Episode


def main() -> None:
    obs = Observation(
        track_id=42,
        class_name="unknown_wheeled_object",
        confidence=0.62,
        distance_m=3.4,
        approaching=True,
        sensor_health=0.91,
        class_history=["wheelchair", "bicycle", "wheelchair", "wheelchair"],
        confidence_history=[0.55, 0.60, 0.70, 0.62],
    )

    uncertainty = UncertaintyEstimator()
    level, u_score, u_reasons = uncertainty.estimate(obs)

    judge = MultiModelJudge()
    verdict = judge.decide(
        [
            Evidence("camera_detector", "mobility_device", 0.78, 0.90),
            Evidence("depth_geometry", "mobility_device", 0.88, 0.95),
            Evidence("vision_language_model", "wheelchair", 0.76, 0.80),
        ]
    )

    decision = SafetyDecisionManager().decide(obs, u_score)

    memory = EpisodicMemory()
    memory.add(
        Episode(
            episode_id="EP_0001",
            embedding=(0.92, 0.15, 0.33),
            semantic_label="mobility_device",
            safety_label="vulnerable_road_user",
            uncertainty="MEDIUM",
            action="SLOW_DOWN",
            outcome="SAFE",
        )
    )
    similar = memory.search((0.90, 0.18, 0.30), top_k=1)

    auto_label = AutoLabelGate().evaluate(
        proposed_label=verdict["label"],
        confidence=verdict["confidence"],
        track_frames=80,
        temporal_consistency=0.93,
        model_agreement=verdict["agreement"],
        safe_fallback_label="unknown_mobility_device",
    )

    print("=== CognitiveDrive AI baseline ===")
    print(f"uncertainty={level} score={u_score:.3f} reasons={u_reasons}")
    print(f"judge={verdict['label']} confidence={verdict['confidence']:.3f}")
    print(f"decision={decision.action} risk={decision.risk} score={decision.score:.3f}")
    if similar:
        episode, similarity = similar[0]
        print(f"memory_match={episode.episode_id} similarity={similarity:.3f}")
    print(
        "auto_label="
        f"{auto_label.label} accepted={auto_label.accepted} reason={auto_label.reason}"
    )


if __name__ == "__main__":
    main()
