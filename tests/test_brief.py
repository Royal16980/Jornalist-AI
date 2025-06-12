import json
from fastapi.testclient import TestClient
import pytest
import types

import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("app", str(Path(__file__).resolve().parents[1] / "app.py"))
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

@pytest.fixture
def client(monkeypatch):
    # stub openai.ChatCompletion.create
    def fake_create(*args, **kwargs):
        assert kwargs.get('model') == 'gpt-4o'
        assert kwargs.get('stream') is True
        data = (
            '{"summary_bullets":["a"],"relevance_score":50,"key_quotes":["q"]}'
        )
        # simulate streaming by yielding chars in two chunks
        chunks = [data[:len(data)//2], data[len(data)//2:]]
        def iterator():
            for chunk in chunks:
                yield {"choices": [{"delta": {"content": chunk}}]}
        return iterator()
    monkeypatch.setattr(app.openai.ChatCompletion, 'create', fake_create)
    return TestClient(app.app)

def test_brief(client):
    payload = {"articles": [{"title": "t", "url": "u", "source": "s", "published_at": "p"}]}
    resp = client.post('/brief', json=payload)
    assert resp.status_code == 200
    text = resp.text
    data = json.loads(text)
    assert data['summary_bullets'] == ['a']
    assert data['relevance_score'] == 50
    assert data['key_quotes'] == ['q']
