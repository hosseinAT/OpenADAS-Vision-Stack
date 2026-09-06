from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class DepthEstimate:
    distance_m: float | None
    valid_pixels: int
    spread_m: float | None
    confidence: float

def robust_bbox_depth(depth_m: np.ndarray, bbox_xyxy: tuple[int,int,int,int], center_ratio: float=0.5, min_depth_m:float=0.15, max_depth_m:float=80.0) -> DepthEstimate:
    if depth_m is None or depth_m.size == 0: return DepthEstimate(None,0,None,0.0)
    h,w=depth_m.shape[:2]; x1,y1,x2,y2=map(int,bbox_xyxy)
    x1=max(0,min(x1,w-1)); x2=max(x1+1,min(x2,w)); y1=max(0,min(y1,h-1)); y2=max(y1+1,min(y2,h))
    ratio=max(0.1,min(float(center_ratio),1.0)); bw=x2-x1; bh=y2-y1
    cx=(x1+x2)//2; cy=(y1+y2)//2; hw=max(1,int(bw*ratio/2)); hh=max(1,int(bh*ratio/2))
    roi=depth_m[max(0,cy-hh):min(h,cy+hh), max(0,cx-hw):min(w,cx+hw)].astype(float)
    vals=roi[np.isfinite(roi) & (roi>=min_depth_m) & (roi<=max_depth_m)]
    if vals.size < 3: return DepthEstimate(None,int(vals.size),None,0.0)
    med=float(np.median(vals)); mad=float(np.median(np.abs(vals-med)))
    if mad>0: vals=vals[np.abs(vals-med)<=3.5*1.4826*mad]
    if vals.size < 3: return DepthEstimate(med,int(vals.size),None,0.2)
    q25,q75=np.percentile(vals,[25,75]); spread=float(q75-q25); med=float(np.median(vals))
    coverage=min(1.0, vals.size/max(20.0, roi.size*0.30)); stability=max(0.0,1.0-min(1.0,spread/max(med,0.1)))
    return DepthEstimate(med,int(vals.size),spread,float(coverage*stability))
