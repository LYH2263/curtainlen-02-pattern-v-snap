from fastapi import HTTPException
from app.engines.curtain_math import fabric_meters
from app.repositories import fabrics, history, settings_repo, windows

def run_estimate(window_id: int, fabric_id: int, save: bool, note: str, pattern_height_cm=None):
    w = windows.get_window(window_id)
    f = fabrics.get_fabric(fabric_id)
    if not w or not f:
        raise HTTPException(404, "not found")
    if w.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty window")
    # 当次传入的花高优先；否则用布料默认花高（厘米 → 米）
    if pattern_height_cm is None:
        pattern_height_cm = f.get("pattern_height_cm") or 0.0
    cm = float(pattern_height_cm)
    pattern_height = cm / 100.0
    settings = settings_repo.get_all()
    fullness = float(w.get("fullness") or settings.get("default_fullness", 2.0))
    calc = fabric_meters(
        w["width"], w["height"], fullness,
        f["hem_top"], f["hem_bottom"], f["fabric_width"],
        pattern_height,
    )
    # 固化当次实际使用的花高（厘米），与结果一并存入快照
    calc["pattern_height_cm"] = round(float(cm), 3)
    run_id = history.insert_run(window_id, fabric_id, calc, note) if save else None
    return {"window": w, "fabric": f, "run_id": run_id, **calc}
