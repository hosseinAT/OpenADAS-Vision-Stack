from openadas.risk import classify_risk
from openadas.types import Track,RiskLevel
CFG={"caution_ttc_s":6.,"warning_ttc_s":4.,"critical_ttc_s":2.5,"critical_distance_m":7.}
def test_critical():
 t=Track(1,"person",(0,0,10,10),(5,5),distance_m=5.); classify_risk(t,CFG); assert t.risk==RiskLevel.CRITICAL
