from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from agents.router import RoutingTable
from backend.deps import get_routing_table

router = APIRouter()


class LanguageOut(BaseModel):
    code: str
    name: str
    script: str
    group: str  # "indian" or "western"


class LanguagesResponse(BaseModel):
    languages: list[LanguageOut]


@router.get("/languages", response_model=LanguagesResponse)
def list_languages(table: RoutingTable = Depends(get_routing_table)) -> LanguagesResponse:
    out: list[LanguageOut] = []
    for lang in table.indian:
        out.append(LanguageOut(code=lang.code, name=lang.name, script=lang.script, group="indian"))
    for lang in table.western:
        out.append(LanguageOut(code=lang.code, name=lang.name, script=lang.script, group="western"))
    return LanguagesResponse(languages=out)
