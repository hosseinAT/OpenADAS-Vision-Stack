from __future__ import annotations
import argparse
from openadas.io import RealSenseSource, assess_camera_health
from openadas.perception import YoloDetector, robust_bbox_depth
from openadas.cognitive.orchestrator import CognitiveDriveOrchestrator

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--model',default='yolo11n.pt'); ap.add_argument('--frames',type=int,default=300); args=ap.parse_args(); detector=YoloDetector(args.model); brain=CognitiveDriveOrchestrator()
    with RealSenseSource() as cam:
        for _ in range(args.frames):
            packet=cam.read(); health=assess_camera_health(packet.rgb,packet.depth_m)
            for j,d in enumerate(detector.predict(packet.rgb)):
                dep=robust_bbox_depth(packet.depth_m,d.bbox_xyxy); result=brain.process(j,d.class_name,d.confidence,dep.distance_m,health.score)
                print(packet.frame_id,j,d.class_name,f'{d.confidence:.2f}',dep.distance_m,result.action,result.uncertainty_level)
if __name__=='__main__': main()
