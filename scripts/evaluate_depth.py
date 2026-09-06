from __future__ import annotations
import argparse,csv,json
from openadas.evaluation import depth_error_metrics

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('csv_path'); args=ap.parse_args(); real=[]; est=[]
    with open(args.csv_path,newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f): real.append(float(row['real_distance_m'])); est.append(float(row['estimated_distance_m']))
    print(json.dumps(depth_error_metrics(real,est),indent=2))
if __name__=='__main__': main()
