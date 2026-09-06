from openadas.cognitive import (
    AutoLabelGate,
    EpisodicMemory,
    Evidence,
    MultiModelJudge,
    Observation,
    SafetyDecisionManager,
    UncertaintyEstimator,
)
from openadas.cognitive.lifecycle import ModelEvaluation, ModelLifecycleGate
from openadas.cognitive.types import Episode


def test_uncertainty_increases_for_unstable_track():
    estimator = UncertaintyEstimator()
    stable = Observation(
        track_id=1,
        class_name="person",
        confidence=0.95,
        class_history=["person"] * 6,
        confidence_history=[0.95, 0.94, 0.96, 0.95],
    )
    unstable = Observation(
        track_id=2,
        class_name="wheelchair",
        confidence=0.55,
        class_history=["wheelchair", "bicycle", "wheelchair", "bicycle"],
        confidence_history=[0.82, 0.42, 0.77, 0.39],
        sensor_health=0.65,
    )
    _, stable_score, _ = estimator.estimate(stable)
    level, unstable_score, reasons = estimator.estimate(unstable)
    assert unstable_score > stable_score
    assert level in {"MEDIUM", "HIGH"}
    assert "class_instability" in reasons


def test_multi_model_judge_uses_dynamic_trust():
    judge = MultiModelJudge()
    result = judge.decide(
        [
            Evidence("camera", "bicycle", 0.90, trust=0.20),
            Evidence("lidar", "mobility_device", 0.88, trust=0.95),
            Evidence("vlm", "mobility_device", 0.85, trust=0.90),
        ]
    )
    assert result["label"] == "mobility_device"
    assert result["confidence"] > 0.80


def test_memory_retrieves_similar_episode():
    memory = EpisodicMemory()
    memory.add(Episode("EP1", (1.0, 0.0), "wheelchair", "vru", "LOW", "SLOW_DOWN"))
    memory.add(Episode("EP2", (0.0, 1.0), "car", "vehicle", "LOW", "CONTINUE"))
    results = memory.search((0.95, 0.05), top_k=1)
    assert results[0][0].episode_id == "EP1"
    assert results[0][1] > 0.9


def test_auto_label_gate_rejects_weak_pseudo_label():
    gate = AutoLabelGate()
    result = gate.evaluate(
        "wheelchair",
        confidence=0.90,
        track_frames=12,
        temporal_consistency=0.95,
        model_agreement=0.90,
        safe_fallback_label="unknown_mobility_device",
    )
    assert result.accepted is False
    assert result.label == "unknown_mobility_device"


def test_decision_manager_requests_caution_for_close_approaching_object():
    manager = SafetyDecisionManager()
    obs = Observation(
        track_id=7,
        class_name="unknown_mobility_device",
        confidence=0.60,
        distance_m=3.0,
        approaching=True,
        sensor_health=0.9,
    )
    decision = manager.decide(obs, uncertainty_score=0.65)
    assert decision.action in {"PREPARE_TO_STOP", "STOP_REQUEST"}
    assert decision.risk in {"HIGH", "CRITICAL"}


def test_model_lifecycle_rejects_regression():
    gate = ModelLifecycleGate()
    bad_candidate = ModelEvaluation(
        old_class_recall_delta=-0.05,
        new_class_recall_delta=0.10,
        calibration_error=0.04,
        latency_ms=45.0,
        shadow_agreement=0.94,
        critical_regressions=0,
    )
    result = gate.evaluate(bad_candidate)
    assert result["promote"] is False
    assert "old_class_regression" in result["failed_checks"]


def test_model_lifecycle_promotes_clean_candidate():
    gate = ModelLifecycleGate()
    good_candidate = ModelEvaluation(
        old_class_recall_delta=-0.005,
        new_class_recall_delta=0.08,
        calibration_error=0.05,
        latency_ms=52.0,
        shadow_agreement=0.95,
        critical_regressions=0,
    )
    result = gate.evaluate(good_candidate)
    assert result["promote"] is True
