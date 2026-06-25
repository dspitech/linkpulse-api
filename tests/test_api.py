from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_link():
    r = client.post("/api/links", json={"url": "https://example.com"})
    assert r.status_code == 201
    data = r.json()
    assert len(data["code"]) == 6
    assert data["clicks"] == 0
    assert data["active"] is True
    assert data["short_url"].endswith(data["code"])


def test_create_link_invalid_url_fails():
    r = client.post("/api/links", json={"url": "not-a-url"})
    assert r.status_code == 422


def test_redirect_found():
    created = client.post("/api/links", json={"url": "https://example.com"}).json()
    r = client.get(f"/r/{created['code']}", follow_redirects=False)
    assert r.status_code == 307
    assert r.headers["location"] == "https://example.com/"


def test_redirect_not_found():
    r = client.get("/r/doesnotexist", follow_redirects=False)
    assert r.status_code == 404


def test_stats_track_clicks():
    created = client.post("/api/links", json={"url": "https://example.com"}).json()
    client.get(f"/r/{created['code']}", follow_redirects=False)
    client.get(f"/r/{created['code']}", follow_redirects=False)
    stats = client.get(f"/api/links/{created['code']}/stats").json()
    assert stats["clicks"] == 2


def test_delete_link_deactivates_it():
    created = client.post("/api/links", json={"url": "https://example.com"}).json()
    r = client.delete(f"/api/links/{created['code']}")
    assert r.status_code == 204
    r2 = client.get(f"/r/{created['code']}", follow_redirects=False)
    assert r2.status_code == 404


def test_delete_unknown_link_returns_404():
    r = client.delete("/api/links/doesnotexist")
    assert r.status_code == 404


def test_list_links_returns_created_link():
    client.post("/api/links", json={"url": "https://example.com"})
    r = client.get("/api/links")
    assert r.status_code == 200
    assert len(r.json()) >= 1
