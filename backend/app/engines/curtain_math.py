from app.engines.helpers import ceil_align, ceil_units


def fabric_meters(
    window_w: float,
    window_h: float,
    fullness: float,
    hem_top: float,
    hem_bottom: float,
    fabric_width: float,
    pattern_height: float = 0.0,
) -> dict:
    if fabric_width <= 0:
        raise ValueError("fabric width required")
    pattern_height = float(pattern_height)
    if pattern_height < 0:
        raise ValueError("pattern height must be >= 0")
    finished_w = float(window_w) * float(fullness)
    panels = max(1, ceil_units(finished_w / float(fabric_width)))
    # 毛裁高 = 层高 + 上下折边
    raw_cut_h = float(window_h) + float(hem_top) + float(hem_bottom)
    # 花高为 0 时不对齐，行为与无花高一致；否则向上对齐到花高的整数倍
    if pattern_height > 0:
        cut_h = ceil_align(raw_cut_h, pattern_height)
    else:
        cut_h = raw_cut_h
    meters = panels * cut_h
    return {
        "finished_width": round(finished_w, 3),
        "panels": panels,
        "pattern_height": round(pattern_height, 6),
        "raw_cut_height": round(raw_cut_h, 3),
        "cut_height": round(cut_h, 3),
        "meters": round(meters, 2),
        "fabric_width": float(fabric_width),
    }
