from __future__ import annotations

import math
from typing import Iterable


def summarize_scan(
    ranges: Iterable[float],
    frame_id: str,
    observed_hz: float,
    age_sec: float,
    *,
    stale_after_sec: float,
) -> dict:
    if age_sec < 0:
        raise ValueError("age_sec must be >= 0")
    if stale_after_sec <= 0:
        raise ValueError("stale_after_sec must be > 0")
    if observed_hz < 0:
        raise ValueError("observed_hz must be >= 0")

    values = list(ranges)
    finite = [float(v) for v in values if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(float(v))]
    available = bool(finite) and age_sec <= stale_after_sec
    return {
        "available": available,
        "frame_id": str(frame_id or ""),
        "sample_count": len(values),
        "finite_count": len(finite),
        "min_range": min(finite) if finite else None,
        "max_range": max(finite) if finite else None,
        "observed_hz": float(observed_hz),
        "age_sec": float(age_sec),
    }
