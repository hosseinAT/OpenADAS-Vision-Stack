from __future__ import annotations
import statistics,time

def benchmark_callable(fn,warmup:int=10,runs:int=50)->dict[str,float]:
    for _ in range(max(0,warmup)): fn()
    samples=[]
    for _ in range(max(1,runs)):
        t=time.perf_counter(); fn(); samples.append((time.perf_counter()-t)*1000)
    s=sorted(samples); p95=s[min(len(s)-1,max(0,int(round(.95*(len(s)-1)))))] ; mean=statistics.fmean(samples)
    return {'mean_latency_ms':mean,'p95_latency_ms':p95,'fps_from_mean':1000.0/mean if mean>0 else float('inf'),'runs':float(len(samples))}
