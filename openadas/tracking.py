from dataclasses import replace
from math import hypot
from .types import Track
class CentroidTracker:
 def __init__(self,max_distance_px=100.0): self.max_distance_px=max_distance_px; self._tracks={}; self._next_id=1
 @staticmethod
 def _center(b): x1,y1,x2,y2=b; return ((x1+x2)/2,(y1+y2)/2)
 def update(self,detections,distances):
  assigned=set(); updated={}
  for det,dist in zip(detections,distances):
   center=self._center(det.bbox); best_id=None; best=float("inf")
   for tid,tr in self._tracks.items():
    if tid in assigned or tr.label!=det.label: continue
    d=hypot(center[0]-tr.center[0],center[1]-tr.center[1])
    if d<best and d<=self.max_distance_px: best_id,best=tid,d
   if best_id is None:
    tid=self._next_id; self._next_id+=1; tr=Track(tid,det.label,det.bbox,center,distance_m=dist)
   else:
    old=self._tracks[best_id]; rel=None if old.distance_m is None or dist is None else dist-old.distance_m
    tr=replace(old,bbox=det.bbox,previous_center=old.center,center=center,previous_distance_m=old.distance_m,distance_m=dist,relative_speed_mps=rel); assigned.add(best_id)
   updated[tr.track_id]=tr
  self._tracks=updated; return list(updated.values())
