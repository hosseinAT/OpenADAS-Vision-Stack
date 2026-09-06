from __future__ import annotations
import json
from pathlib import Path

def write_experiment_report(path:str|Path,title:str,metrics:dict,environment:dict|None=None,notes:list[str]|None=None)->Path:
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); payload={'title':title,'metrics':metrics,'environment':environment or {},'notes':notes or []}; p.write_text(json.dumps(payload,indent=2,sort_keys=True),encoding='utf-8'); return p
