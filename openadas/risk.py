from .types import RiskLevel
from .distance import calculate_ttc
def classify_risk(track,cfg):
 track.ttc_s=calculate_ttc(track.distance_m,track.relative_speed_mps)
 if track.distance_m is not None and track.distance_m<=cfg["critical_distance_m"]: track.risk=RiskLevel.CRITICAL
 elif track.ttc_s is None: track.risk=RiskLevel.SAFE
 elif track.ttc_s<=cfg["critical_ttc_s"]: track.risk=RiskLevel.CRITICAL
 elif track.ttc_s<=cfg["warning_ttc_s"]: track.risk=RiskLevel.WARNING
 elif track.ttc_s<=cfg["caution_ttc_s"]: track.risk=RiskLevel.CAUTION
 else: track.risk=RiskLevel.SAFE
 return track
