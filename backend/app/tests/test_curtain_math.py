from app.engines.curtain_math import fabric_meters
import pytest

def test_living_room():
    r = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4)
    assert r["panels"] == 5
    assert r["cut_height"] == 2.85
    assert r["meters"] == 14.25
    # 花高为 0：毛裁高即裁高
    assert r["pattern_height"] == 0.0
    assert r["raw_cut_height"] == 2.85

def test_single_panel_narrow():
    r = fabric_meters(1.0, 2.0, 1.5, 0.0, 0.0, 2.8)
    assert r["panels"] == 1
    assert r["meters"] == 2.0

def test_pattern_height_rounds_up():
    # 毛裁高 2.85m，花高 0.64m → 向上对齐到 3.20m
    r = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, 0.64)
    assert r["raw_cut_height"] == 2.85
    assert r["cut_height"] == 3.2
    assert r["panels"] == 5
    assert r["meters"] == 16.0
    assert r["pattern_height"] == 0.64

def test_exact_multiple_not_overshot():
    # 2.85 / 0.95 == 3 恰为整数倍，不应被浮点误差多抬到 3.8
    r = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, 0.95)
    assert r["cut_height"] == 2.85
    assert r["meters"] == 14.25

def test_small_raw_aligns_to_at_least_one_pattern():
    # 毛裁高 0.5m 小于花高 0.64m → 一整个花高
    r = fabric_meters(1.0, 0.4, 1.0, 0.05, 0.05, 2.8, 0.64)
    assert r["raw_cut_height"] == 0.5
    assert r["cut_height"] == 0.64

def test_negative_pattern_height_rejected():
    with pytest.raises(ValueError):
        fabric_meters(1.0, 2.0, 2.0, 0.1, 0.1, 1.4, -0.5)
