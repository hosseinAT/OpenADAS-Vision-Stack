import argparse,cv2
from openadas.config import load_config
from openadas.pipeline import OpenADASPipeline
def main():
 p=argparse.ArgumentParser(); p.add_argument("--input",required=True); p.add_argument("--output",default="output.mp4"); a=p.parse_args(); cap=cv2.VideoCapture(a.input)
 if not cap.isOpened(): raise RuntimeError(f"Video kann nicht geöffnet werden: {a.input}")
 fps=cap.get(cv2.CAP_PROP_FPS) or 25.; w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)); wr=cv2.VideoWriter(a.output,cv2.VideoWriter_fourcc(*"mp4v"),fps,(w,h)); pipe=OpenADASPipeline(load_config())
 while True:
  ok,frame=cap.read()
  if not ok: break
  out,_,_=pipe.process(frame,[]); wr.write(out)
 cap.release(); wr.release(); print(f"Gespeichert: {a.output}")
if __name__=="__main__": main()
