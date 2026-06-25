"""Point d'entree FastAPI de LinkPulse.
Expose :
- /health
- /metrics
- /api/links
- /api/links/{code}/stats
- /r/{code}
- /api/links/{code} (DELETE)
"""

import os
from time import perf_counter

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import RedirectResponse
from prometheus_client import Counter, Gauge, Histogram
from prometheus_fastapi_instrumentator import Instrumentator

from src import storage
from src.schemas import LinkCreateRequest, LinkResponse, LinkStatsResponse
from src.shortener import generate_unique_code

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")

app = FastAPI(title="LinkPulse", version="0.1.0")

storage.init_db()

# --- Metrics ---
links_created_total = Counter(
    "links_created_total",
    "Nombre total de liens courts crees",
)

redirects_total = Counter(
    "redirects_total",
    "Nombre total de tentatives de redirection",
    ["status"],
)

redirect_duration = Histogram(
    "redirect_duration_seconds",
    "Duree de traitement d'une redirection",
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5],
)

active_links_gauge = Gauge(
    "active_links_gauge",
    "Nombre de liens actifs actuellement en base",
)

Instrumentator().instrument(app).expose(app)


def _to_link_response(link: dict) -> LinkResponse:
    return LinkResponse(
        code=link["code"],
        url=link["url"],
        short_url=f"{BASE_URL}/r/{link['code']}",
        created_at=link["created_at"],
        clicks=link["clicks"],
        active=bool(link["active"]),
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/links", response_model=LinkResponse, status_code=201)
def create_link(payload: LinkCreateRequest):
    code = generate_unique_code()

    try:
        link = storage.create_link(code, str(payload.url))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur creation lien") from e

    links_created_total.inc()
    active_links_gauge.set(storage.count_active_links())

    return _to_link_response(link)


@app.get("/api/links", response_model=list[LinkResponse])
def get_links(skip: int = 0, limit: int = 20):
    links = storage.list_links(skip=skip, limit=limit)
    return [_to_link_response(link) for link in links]


@app.get("/api/links/{code}/stats", response_model=LinkStatsResponse)
def link_stats(code: str):
    link = storage.get_link(code)

    if not link:
        raise HTTPException(status_code=404, detail="Lien introuvable")

    return LinkStatsResponse(
        code=link["code"],
        url=link["url"],
        created_at=link["created_at"],
        clicks=link["clicks"],
        active=bool(link["active"]),
    )


@app.delete("/api/links/{code}", status_code=204)
def delete_link(code: str):
    ok = storage.deactivate_link(code)

    if not ok:
        raise HTTPException(status_code=404, detail="Lien introuvable")

    active_links_gauge.set(storage.count_active_links())
    return Response(status_code=204)


@app.get("/r/{code}")
def redirect_to_url(code: str):
    start = perf_counter()

    link = storage.get_link(code)

    if not link or not link["active"]:
        redirects_total.labels(status="not_found").inc()
        redirect_duration.observe(perf_counter() - start)

        raise HTTPException(
            status_code=404,
            detail="Lien introuvable ou desactive",
        )

    storage.increment_clicks(code)

    redirects_total.labels(status="found").inc()
    redirect_duration.observe(perf_counter() - start)

    return RedirectResponse(
        url=link["url"],
        status_code=307,
    )
