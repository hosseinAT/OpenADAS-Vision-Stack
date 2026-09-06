from openadas.cognitive import Episode
from openadas.cognitive.orchestrator import CognitiveDriveOrchestrator
from openadas.perception.features import compact_episode_embedding
brain=CognitiveDriveOrchestrator(); emb=compact_episode_embedding('mobility_device',.95,4.0,1.0,None); brain.remember(Episode('EP_DEMO_001',emb,'mobility_device','vulnerable_road_user','LOW','SLOW_DOWN','SAFE'))
for frame in range(35): result=brain.process(7,'mobility_device',.94,5.0-frame*.04,1.0)
print(result)
