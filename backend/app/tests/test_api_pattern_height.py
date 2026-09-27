import json

from conftest import count_runs


def test_preview_does_not_insert(client):
    before = count_runs()
    r = client.get("/api/estimate", params={"window_id": 1, "fabric_id": 1})
    assert r.status_code == 200
    body = r.json()
    assert body["run_id"] is None
    assert body["pattern_height_cm"] == 64
    assert body["raw_cut_height"] == 2.85
    assert body["cut_height"] == 3.2
    assert count_runs() == before


def test_preview_with_override(client):
    r = client.get("/api/estimate", params={"window_id": 2, "fabric_id": 1, "pattern_height_cm": 95})
    assert r.status_code == 200
    body = r.json()
    # 1.5 + 0.10 + 0.15 = 1.75，向上对齐 0.95 的倍数 → 1.9
    assert body["pattern_height_cm"] == 95
    assert body["raw_cut_height"] == 1.75
    assert body["cut_height"] == 1.9
    assert body["meters"] == round(body["panels"] * 1.9, 2)


def test_negative_pattern_height_get_422_and_no_row(client):
    before = count_runs()
    r = client.get("/api/estimate", params={"window_id": 1, "fabric_id": 1, "pattern_height_cm": -10})
    assert r.status_code == 422
    assert count_runs() == before


def test_negative_pattern_height_post_422_and_no_row(client):
    before = count_runs()
    r = client.post("/api/estimate", json={
        "window_id": 1, "fabric_id": 1, "pattern_height_cm": -10, "save": True,
    })
    assert r.status_code == 422
    assert count_runs() == before


def test_save_persists_snapshot(client):
    r = client.post("/api/estimate", json={
        "window_id": 1, "fabric_id": 1, "pattern_height_cm": 64, "save": True, "note": "对花",
    })
    assert r.status_code == 200
    run_id = r.json()["run_id"]
    assert run_id is not None

    runs = client.get("/api/runs").json()["items"]
    saved = next(x for x in runs if x["id"] == run_id)
    snap = saved["result"]
    assert snap["pattern_height_cm"] == 64
    assert snap["raw_cut_height"] == 2.85
    assert snap["cut_height"] == 3.2
    assert snap["meters"] == 16.0


def test_changing_fabric_default_does_not_rewrite_old_run(client):
    # 以 64cm 花高保存编号
    r = client.post("/api/estimate", json={
        "window_id": 1, "fabric_id": 1, "pattern_height_cm": 64, "save": True,
    })
    run_id = r.json()["run_id"]

    # 事后把布料默认花高改为 100cm
    p = client.patch("/api/fabrics/1", json={"pattern_height_cm": 100})
    assert p.status_code == 200
    assert p.json()["pattern_height_cm"] == 100

    # 按编号回看仍是当初对齐后的 3.2m，而非按新花高重算
    runs = client.get("/api/runs").json()["items"]
    snap = next(x for x in runs if x["id"] == run_id)["result"]
    assert snap["pattern_height_cm"] == 64
    assert snap["cut_height"] == 3.2
    assert snap["meters"] == 16.0

    # 新试算则跟随新默认花高：2.85 向上对齐 1.0 → 3.0
    r2 = client.get("/api/estimate", params={"window_id": 1, "fabric_id": 1})
    assert r2.json()["pattern_height_cm"] == 100
    assert r2.json()["cut_height"] == 3.0


def test_patch_negative_rejected(client):
    r = client.patch("/api/fabrics/1", json={"pattern_height_cm": -1})
    assert r.status_code == 422
