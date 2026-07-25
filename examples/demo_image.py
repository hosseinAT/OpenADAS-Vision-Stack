import cv2, numpy as np
from openadas.config import load_config
from openadas.pipeline import OpenADASPipeline
from openadas.types import Detection
def main():
 h,w=720,1280; img=np.zeros((h,w,3),dtype=np.uint8); img[:]=(55,55,55); cv2.fillPoly(img,[np.array([[180,h],[500,390],[780,390],[1100,h]],np.int32)],(70,70,70)); cv2.line(img,(350,h),(560,390),(255,255,255),10); cv2.line(img,(930,h),(720,390),(255,255,255),10)
 pipe=OpenADASPipeline(load_config()); pipe.process(img,[Detection("wheelchair_user",.94,(570,410,690,600),.9)]); out,lane,tracks=pipe.process(img,[Detection("wheelchair_user",.95,(555,390,705,620),.9)])
 print(f"lane_status={lane.status}"); [print(f"object={t.label}, distance_m={t.distance_m:.2f}, ttc_s={t.ttc_s}, risk={t.risk.value}") for t in tracks]; cv2.imwrite("demo_output.jpg",out); print("Gespeichert: demo_output.jpg")
if __name__=="__main__": main()
