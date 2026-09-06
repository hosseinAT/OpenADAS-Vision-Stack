from __future__ import annotations
from dataclasses import dataclass
import numpy as np
@dataclass(frozen=True)
class ClassificationMetrics:
    precision: float; recall: float; f1: float

def binary_metrics(y_true,y_pred,positive=1)->ClassificationMetrics:
    yt=np.asarray(y_true); yp=np.asarray(y_pred); tp=int(np.sum((yt==positive)&(yp==positive))); fp=int(np.sum((yt!=positive)&(yp==positive))); fn=int(np.sum((yt==positive)&(yp!=positive)))
    p=tp/(tp+fp) if tp+fp else 0.0; r=tp/(tp+fn) if tp+fn else 0.0; f=2*p*r/(p+r) if p+r else 0.0; return ClassificationMetrics(p,r,f)

def expected_calibration_error(confidences,correctness,bins:int=10)->float:
    c=np.asarray(confidences,dtype=float); y=np.asarray(correctness,dtype=float)
    if c.size==0:return 0.0
    edges=np.linspace(0,1,bins+1); ece=0.0
    for i in range(bins):
        mask=(c>=edges[i]) & ((c<edges[i+1]) if i<bins-1 else (c<=edges[i+1]))
        if np.any(mask): ece += float(np.mean(mask))*abs(float(np.mean(c[mask]))-float(np.mean(y[mask])))
    return float(ece)

def depth_error_metrics(real_m,estimated_m)->dict[str,float]:
    r=np.asarray(real_m,dtype=float); e=np.asarray(estimated_m,dtype=float); mask=np.isfinite(r)&np.isfinite(e)
    if not np.any(mask):return {'mae_m':float('nan'),'rmse_m':float('nan'),'mape_pct':float('nan')}
    d=e[mask]-r[mask]; denom=np.maximum(np.abs(r[mask]),1e-6); return {'mae_m':float(np.mean(np.abs(d))),'rmse_m':float(np.sqrt(np.mean(d*d))),'mape_pct':float(np.mean(np.abs(d)/denom)*100)}
