from __future__ import annotations

import cv2
import numpy as np

from .types import LaneResult


def _avg(lines: list[tuple[int, int, int, int]]):
    """Return the average line or None when no line is available."""
    if not lines:
        return None
    arr = np.asarray(lines, dtype=np.float32).reshape(-1, 4)
    return tuple(int(v) for v in np.mean(arr, axis=0))


def _unpack_hough_line(raw) -> tuple[int, int, int, int] | None:
    """Normalize OpenCV HoughLinesP output across OpenCV versions.

    Depending on the OpenCV build, one entry can have shape ``(1, 4)``
    or ``(4,)``. Flattening makes both formats safe to process.
    """
    values = np.asarray(raw).reshape(-1)
    if values.size != 4:
        return None
    return tuple(int(v) for v in values)


def detect_lanes(frame: np.ndarray, cfg: dict):
    h, w = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, cfg["canny_low"], cfg["canny_high"])

    top = int(h * cfg["roi_top_ratio"])
    mask = np.zeros_like(edges)
    polygon = np.array(
        [[(0, h), (int(w * 0.42), top), (int(w * 0.58), top), (w, h)]],
        dtype=np.int32,
    )
    cv2.fillPoly(mask, polygon, 255)
    roi = cv2.bitwise_and(edges, mask)

    lines = cv2.HoughLinesP(
        roi,
        1,
        np.pi / 180,
        cfg["hough_threshold"],
        minLineLength=cfg["min_line_length"],
        maxLineGap=cfg["max_line_gap"],
    )

    left: list[tuple[int, int, int, int]] = []
    right: list[tuple[int, int, int, int]] = []

    if lines is not None:
        for raw in lines:
            unpacked = _unpack_hough_line(raw)
            if unpacked is None:
                continue

            x1, y1, x2, y2 = unpacked
            if x2 == x1:
                continue

            slope = (y2 - y1) / (x2 - x1)
            if abs(slope) < 0.35:
                continue

            midpoint_x = (x1 + x2) / 2.0
            if slope < 0 and midpoint_x < w / 2:
                left.append(unpacked)
            elif slope > 0 and midpoint_x > w / 2:
                right.append(unpacked)

    left_line = _avg(left)
    right_line = _avg(right)
    center = None
    offset = None
    confidence = 0.0
    status = "LANE_LOST"

    if left_line and right_line:
        left_bottom_x = max(left_line[0], left_line[2])
        right_bottom_x = min(right_line[0], right_line[2])
        pixel_lane_width = right_bottom_x - left_bottom_x

        if pixel_lane_width > 0:
            center = (left_bottom_x + right_bottom_x) / 2.0
            meters_per_pixel = cfg["lane_width_m"] / pixel_lane_width
            offset = (w / 2.0 - center) * meters_per_pixel
            confidence = min(1.0, 0.5 + 0.05 * min(len(left), len(right)))
            status = (
                "SAFE"
                if abs(offset) < 0.25
                else "WARNING"
                if abs(offset) < 0.45
                else "LANE_DEPARTURE"
            )

    output = frame.copy()
    for line in (left_line, right_line):
        if line:
            cv2.line(
                output,
                (line[0], line[1]),
                (line[2], line[3]),
                (0, 255, 0),
                5,
            )

    if center is not None:
        cv2.line(output, (int(center), h), (int(center), top), (255, 255, 0), 2)
        cv2.line(output, (w // 2, h), (w // 2, top), (0, 0, 255), 2)

    return LaneResult(
        left_line,
        right_line,
        center,
        offset,
        confidence,
        status,
    ), output
