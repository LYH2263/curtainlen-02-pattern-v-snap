import os
import tempfile

# 必须在导入 app.config 之前指定独立的测试数据库目录
os.environ.setdefault("DATA_DIR", tempfile.mkdtemp(prefix="curtainlen-test-"))

import pytest
from fastapi.testclient import TestClient

from app import seed
from app.db import connect
from app.main import app


def _reset_db():
    c = connect()
    try:
        c.execute("DELETE FROM calc_runs")
        c.execute("UPDATE fabrics SET pattern_height_cm=0 WHERE name='纱帘2.8m'")
        c.execute("UPDATE fabrics SET pattern_height_cm=64 WHERE name='遮光1.4m'")
        c.commit()
    finally:
        c.close()


def count_runs() -> int:
    c = connect()
    try:
        return c.execute("SELECT COUNT(*) c FROM calc_runs").fetchone()["c"]
    finally:
        c.close()


@pytest.fixture()
def client():
    seed.init_db()
    _reset_db()
    with TestClient(app) as c:
        yield c
