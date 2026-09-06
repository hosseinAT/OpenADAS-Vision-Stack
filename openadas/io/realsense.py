from __future__ import annotations
import time
from .interfaces import CameraPacket

class RealSenseSource:
    """Lazy RealSense D4xx adapter. pyrealsense2 is imported only on start()."""
    def __init__(self, width:int=640, height:int=480, fps:int=30):
        self.width=width; self.height=height; self.fps=fps
        self._pipeline=None; self._align=None; self._frame_id=0
    def start(self)->None:
        try:
            import pyrealsense2 as rs
        except ImportError as exc:
            raise RuntimeError('pyrealsense2 is required for RealSense hardware. Install librealsense/pyrealsense2 first.') from exc
        pipeline=rs.pipeline(); config=rs.config()
        config.enable_stream(rs.stream.color,self.width,self.height,rs.format.bgr8,self.fps)
        config.enable_stream(rs.stream.depth,self.width,self.height,rs.format.z16,self.fps)
        profile=pipeline.start(config)
        self._pipeline=pipeline; self._align=rs.align(rs.stream.color)
        self._depth_scale=profile.get_device().first_depth_sensor().get_depth_scale()
        cprof=profile.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()
        self._intrinsics={'fx':float(cprof.fx),'fy':float(cprof.fy),'ppx':float(cprof.ppx),'ppy':float(cprof.ppy)}
    def read(self, timeout_ms:int=5000)->CameraPacket:
        if self._pipeline is None: raise RuntimeError('RealSenseSource.start() must be called before read().')
        import numpy as np
        frames=self._align.process(self._pipeline.wait_for_frames(timeout_ms))
        color=frames.get_color_frame(); depth=frames.get_depth_frame()
        if not color or not depth: raise RuntimeError('Incomplete RealSense frame set.')
        rgb=np.asanyarray(color.get_data())
        depth_m=np.asanyarray(depth.get_data()).astype('float32')*float(self._depth_scale)
        self._frame_id += 1
        ts=float(color.get_timestamp())/1000.0 if color.get_timestamp() else time.time()
        return CameraPacket(rgb,depth_m,ts,self._frame_id,dict(self._intrinsics),{'source':'realsense'})
    def stop(self)->None:
        if self._pipeline is not None: self._pipeline.stop(); self._pipeline=None
    def __enter__(self): self.start(); return self
    def __exit__(self, exc_type, exc, tb): self.stop()
