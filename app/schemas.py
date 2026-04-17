import re
from pydantic import BaseModel, field_validator

SECTOR_RE = re.compile(r"^[a-zA-Z][a-zA-Z\s\-&]{1,39}$")


class SectorIn(BaseModel):
    sector: str

    @field_validator("sector")
    @classmethod
    def check_sector(cls, v: str) -> str:
        v = v.strip()
        if not SECTOR_RE.match(v):
            raise ValueError("sector must be 2-40 chars, letters/spaces/-/& only")
        return v.lower()


class AnalyzeResponse(BaseModel):
    sector: str
    generated_at: str
    report_markdown: str
    sources: list[str]
    usage: dict
