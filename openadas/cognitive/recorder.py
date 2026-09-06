from __future__ import annotations
import json,time
from pathlib import Path
import numpy as np
from .types import Episode

class EpisodeRecorder:
    """Writes auditable episode metadata and optional raw sensor arrays."""
    def __init__(self,root:str|Path='data/episodes'): self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
    def record(self,episode:Episode,rgb=None,depth_m=None,extra:dict|None=None)->Path:
        folder=self.root/episode.episode_id; folder.mkdir(parents=True,exist_ok=True)
        payload={'episode_id':episode.episode_id,'semantic_label':episode.semantic_label,'safety_label':episode.safety_label,'uncertainty':episode.uncertainty,'action':episode.action,'outcome':episode.outcome,'embedding':list(episode.embedding),'metadata':episode.metadata,'recorded_unix_s':time.time(),'extra':extra or {}}
        (folder/'episode.json').write_text(json.dumps(payload,indent=2,sort_keys=True),encoding='utf-8')
        if rgb is not None: np.save(folder/'rgb.npy',np.asarray(rgb))
        if depth_m is not None: np.save(folder/'depth_m.npy',np.asarray(depth_m,dtype=np.float32))
        return folder
