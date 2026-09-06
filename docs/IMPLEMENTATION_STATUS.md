# CognitiveDrive AI — Implementation Status

This file is the source of truth for what is implemented, what is simulated, and what still requires physical validation.

| Capability | Status | Evidence / acceptance criterion |
|---|---|---|
| Existing OpenADAS lane/risk baseline | Implemented | Existing tests and demo |
| Cognitive uncertainty baseline | Implemented | Unit-tested temporal confidence/class stability logic |
| Multi-model trust-weighted judge | Implemented baseline | Unit tests and synthetic demo |
| Advisory safety decision manager | Implemented baseline | Unit tests |
| Episodic vector memory | Implemented baseline | Similarity retrieval tests |
| Auto-label acceptance gate | Implemented baseline | Conservative rule tests |
| Candidate model promotion gate | Implemented baseline | Regression/shadow/latency gate tests |
| RealSense RGB/depth adapter | Implemented in software | Requires D456C physical validation |
| Robust depth association | Implemented in software | Synthetic tests; requires physical calibration |
| YOLO detector adapter | Implemented in software | Requires optional Ultralytics dependency/model weights |
| Track history / motion trend | Implemented in software | Synthetic tests |
| End-to-end recorded-frame pipeline | Implemented in software | Synthetic/mock sensor test |
| SQLite episodic persistence | Implemented in software | Unit-tested local database behavior |
| Dataset/episode recorder | Implemented in software | Unit-tested metadata and file layout |
| Evaluation metrics/reporting | Implemented in software | Unit-tested metric calculations |
| ROS2 node integration | Scaffold + interface contract | Requires ROS2 Humble runtime validation |
| CARLA scenario integration | Scaffold + scenario specification | Requires CARLA runtime/GPU validation |
| ONNX/TensorRT deployment | Export/benchmark scripts scaffold | Requires compatible GPU/Jetson runtime |
| LiDAR adapter/fusion | Interface + mock baseline | Requires selected physical LiDAR and calibration |
| Radar adapter/fusion | Interface + mock baseline | Requires selected physical radar and driver |
| Multi-camera 360° rig | Architecture only | Requires hardware, calibration and synchronization |
| RC/mobile platform | Architecture only | Requires hardware, motor controller and safety stop |
| Real-road autonomous control | Not in scope | This repository is a research/portfolio demonstrator |

## Integrity rule

No README, CV, interview statement or project report should claim a hardware feature as validated until its acceptance evidence is committed under `experiments/` or `docs/results/`.