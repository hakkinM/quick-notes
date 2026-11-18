import pytest


@pytest.fixture(autouse=True)
def isolate_env(monkeypatch):
    monkeypatch.delenv("QNOTES_PATH", raising=False)
