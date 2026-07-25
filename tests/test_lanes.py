import cv2
import numpy as np

from openadas.lanes import _unpack_hough_line, detect_lanes


CFG = {
    "roi_top_ratio": 0.60,
    "canny_low": 70,
    "canny_high": 160,
    "hough_threshold": 35,
    "min_line_length": 35,
    "max_line_gap": 70,
    "lane_width_m": 3.5,
}


def test_unpack_hough_line_accepts_both_common_shapes():
    assert _unpack_hough_line(np.array([1, 2, 3, 4], dtype=np.int32)) == (1, 2, 3, 4)
    assert _unpack_hough_line(np.array([[1, 2, 3, 4]], dtype=np.int32)) == (1, 2, 3, 4)


def test_detect_lanes_does_not_crash_on_synthetic_frame():
    height, width = 720, 1280
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    frame[:] = (55, 55, 55)
    cv2.line(frame, (350, height), (560, 390), (255, 255, 255), 10)
    cv2.line(frame, (930, height), (720, 390), (255, 255, 255), 10)

    result, output = detect_lanes(frame, CFG)

    assert output.shape == frame.shape
    assert result.status in {"SAFE", "WARNING", "LANE_DEPARTURE", "LANE_LOST"}
