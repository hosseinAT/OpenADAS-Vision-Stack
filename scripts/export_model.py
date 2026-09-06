from __future__ import annotations
import argparse
from openadas.deployment import export_ultralytics_onnx, export_ultralytics_tensorrt

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('model'); ap.add_argument('--format',choices=['onnx','engine'],default='onnx'); args=ap.parse_args(); print(export_ultralytics_onnx(args.model) if args.format=='onnx' else export_ultralytics_tensorrt(args.model))
if __name__=='__main__': main()
