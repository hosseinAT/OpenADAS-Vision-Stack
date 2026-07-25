from .lanes import detect_lanes
from .distance import estimate_distance_m
from .tracking import CentroidTracker
from .risk import classify_risk
from .visualization import draw_dashboard
class OpenADASPipeline:
 def __init__(self,config): self.config=config; self.tracker=CentroidTracker()
 def process(self,frame,detections):
  lane,overlay=detect_lanes(frame,self.config["lane"]); distances=[estimate_distance_m(d,self.config["camera"]["focal_length_px"]) for d in detections]; tracks=self.tracker.update(detections,distances); tracks=[classify_risk(t,self.config["risk"]) for t in tracks]; return draw_dashboard(overlay,lane,tracks),lane,tracks
