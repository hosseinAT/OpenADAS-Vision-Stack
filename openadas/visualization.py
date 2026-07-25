import cv2
def draw_dashboard(frame,lane,tracks):
 out=frame.copy(); h,w=out.shape[:2]; cv2.rectangle(out,(0,0),(w,90),(20,20,20),-1); txt=f"Lane: {lane.status} | confidence={lane.confidence:.2f}"
 if lane.offset_m is not None: txt+=f" | offset={lane.offset_m:+.2f} m"
 cv2.putText(out,txt,(20,32),cv2.FONT_HERSHEY_SIMPLEX,.65,(255,255,255),2)
 for tr in tracks:
  x1,y1,x2,y2=tr.bbox; color=(0,255,0) if tr.risk.value=="SAFE" else (0,0,255); cv2.rectangle(out,(x1,y1),(x2,y2),color,2); label=f"{tr.label} #{tr.track_id} {tr.distance_m:.1f}m {tr.risk.value}"; cv2.putText(out,label,(x1,max(20,y1-8)),cv2.FONT_HERSHEY_SIMPLEX,.52,color,2)
 return out
