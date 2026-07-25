from openadas.tracking import CentroidTracker
from openadas.types import Detection
def test_id():
 tr=CentroidTracker(50); a=tr.update([Detection("car",.9,(0,0,20,20))],[10.])[0]; b=tr.update([Detection("car",.9,(5,0,25,20))],[9.])[0]; assert a.track_id==b.track_id and b.relative_speed_mps==-1.
