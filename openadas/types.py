from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple
BBox=Tuple[int,int,int,int]
class RiskLevel(str,Enum):
 SAFE="SAFE"; CAUTION="CAUTION"; WARNING="WARNING"; CRITICAL="CRITICAL"
@dataclass
class Detection:
 label:str; confidence:float; bbox:BBox; real_width_m:float=1.8
@dataclass
class Track:
 track_id:int; label:str; bbox:BBox; center:Tuple[float,float]; previous_center:Optional[Tuple[float,float]]=None; distance_m:Optional[float]=None; previous_distance_m:Optional[float]=None; relative_speed_mps:Optional[float]=None; ttc_s:Optional[float]=None; risk:RiskLevel=RiskLevel.SAFE
@dataclass
class LaneResult:
 left_line:Optional[Tuple[int,int,int,int]]; right_line:Optional[Tuple[int,int,int,int]]; lane_center_x:Optional[float]; offset_m:Optional[float]; confidence:float; status:str
