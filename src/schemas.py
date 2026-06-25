"""Schemas Pydantic - contrats d'entree/sortie de l'API LinkPulse."""

from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl


class LinkCreateRequest(BaseModel):
    url: HttpUrl = Field(..., description="URL longue a raccourcir")


class LinkBaseResponse(BaseModel):
    code: str
    url: str
    created_at: datetime
    clicks: int
    active: bool


class LinkResponse(LinkBaseResponse):
    short_url: str


class LinkStatsResponse(LinkBaseResponse):
    pass
