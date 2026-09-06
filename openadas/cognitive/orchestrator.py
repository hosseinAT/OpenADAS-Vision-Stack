from __future__ import annotations
from dataclasses import dataclass
from .types import Observation, Evidence, Episode
from .uncertainty import UncertaintyEstimator
from .judge import MultiModelJudge
from .decision import SafetyDecisionManager
from .memory import EpisodicMemory
from .autolabel import AutoLabelGate
from openadas.perception.track_history import TrackHistoryStore
from openadas.perception.features import compact_episode_embedding
from openadas.fusion import memory_evidence

@dataclass(frozen=True)
class CognitiveResult:
    track_id: int; semantic_label: str; uncertainty_level: str; uncertainty_score: float; action: str; risk: str
    memory_match: str|None; memory_similarity: float; auto_label: str; auto_label_accepted: bool; reason: str

class CognitiveDriveOrchestrator:
    def __init__(self,memory=None):
        self.histories=TrackHistoryStore(maxlen=60); self.uncertainty=UncertaintyEstimator(); self.judge=MultiModelJudge(); self.decision=SafetyDecisionManager(); self.memory=memory or EpisodicMemory(); self.autolabel=AutoLabelGate()
    def process(self,track_id:int,class_name:str,confidence:float,distance_m:float|None,sensor_health:float=1.0,additional_evidence:list[Evidence]|None=None)->CognitiveResult:
        hist=self.histories.update(track_id,class_name,confidence,distance_m)
        obs=Observation(track_id,class_name,confidence,distance_m,hist.approaching,sensor_health,list(hist.classes),list(hist.confidences))
        level,u_score,u_reasons=self.uncertainty.estimate(obs); emb=compact_episode_embedding(class_name,confidence,distance_m,sensor_health,hist)
        matches=self.memory.search(emb,top_k=1) if len(self.memory) else []; evidences=[Evidence('primary_detector',class_name,confidence,trust=sensor_health)] + list(additional_evidence or [])
        match_id=None; match_sim=0.0
        if matches:
            ep,match_sim=matches[0]; match_id=ep.episode_id; mev=memory_evidence(ep.semantic_label,match_sim)
            if mev: evidences.append(mev)
        judged=self.judge.decide(evidences); decision=self.decision.decide(obs,u_score)
        auto=self.autolabel.evaluate(judged['label'],judged['confidence'],hist.frames,hist.temporal_consistency,judged['agreement'],safe_fallback_label='unknown_object')
        return CognitiveResult(track_id,judged['label'],level,u_score,decision.action,decision.risk,match_id,float(match_sim),auto.label,auto.accepted,';'.join(u_reasons+[decision.reason]))
    def remember(self,episode:Episode)->None: self.memory.add(episode)
