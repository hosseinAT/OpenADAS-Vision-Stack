from __future__ import annotations
import json, sqlite3
from pathlib import Path
from .types import Episode
from .memory import _cosine

class SQLiteEpisodicMemory:
    """Persistent dependency-light episodic memory for portfolio-scale experiments."""
    def __init__(self,path:str|Path='data/memory/episodes.sqlite3'):
        self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True); self.conn=sqlite3.connect(self.path)
        self.conn.execute('''CREATE TABLE IF NOT EXISTS episodes(episode_id TEXT PRIMARY KEY, embedding TEXT NOT NULL, semantic_label TEXT NOT NULL, safety_label TEXT NOT NULL, uncertainty TEXT NOT NULL, action TEXT NOT NULL, outcome TEXT NOT NULL, metadata TEXT NOT NULL)'''); self.conn.commit()
    def add(self,episode:Episode)->None:
        self.conn.execute('INSERT OR REPLACE INTO episodes VALUES(?,?,?,?,?,?,?,?)',(episode.episode_id,json.dumps(list(episode.embedding)),episode.semantic_label,episode.safety_label,episode.uncertainty,episode.action,episode.outcome,json.dumps(episode.metadata,sort_keys=True))); self.conn.commit()
    def search(self,embedding:tuple[float,...],top_k:int=3)->list[tuple[Episode,float]]:
        scored=[]
        for row in self.conn.execute('SELECT * FROM episodes').fetchall():
            ep=Episode(row[0],tuple(json.loads(row[1])),row[2],row[3],row[4],row[5],row[6],json.loads(row[7])); scored.append((ep,_cosine(embedding,ep.embedding)))
        scored.sort(key=lambda x:x[1],reverse=True); return scored[:max(0,int(top_k))]
    def __len__(self)->int: return int(self.conn.execute('SELECT COUNT(*) FROM episodes').fetchone()[0])
    def close(self)->None: self.conn.close()
    def __enter__(self): return self
    def __exit__(self,exc_type,exc,tb): self.close()
