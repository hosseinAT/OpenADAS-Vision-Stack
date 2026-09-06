"""CognitiveDrive research modules.

The package contains safety-oriented prototype building blocks for uncertainty,
multi-evidence judging, episodic memory, auto-label gating and model lifecycle.
These modules are designed for research/demonstration and are not certified
for control of a real road vehicle.
"""

from .types import Evidence, Observation, Decision, Episode
from .uncertainty import UncertaintyEstimator
from .judge import MultiModelJudge
from .decision import SafetyDecisionManager
from .memory import EpisodicMemory
from .autolabel import AutoLabelGate
from .lifecycle import ModelLifecycleGate

__all__ = [
    "Evidence",
    "Observation",
    "Decision",
    "Episode",
    "UncertaintyEstimator",
    "MultiModelJudge",
    "SafetyDecisionManager",
    "EpisodicMemory",
    "AutoLabelGate",
    "ModelLifecycleGate",
]
