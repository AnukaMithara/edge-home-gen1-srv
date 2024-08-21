from typing import Optional

from pydantic import BaseModel


class SourceModel(BaseModel):
    source_name: str
    display_name: str
    credibility: Optional[int] = None
    source_category: Optional[int] = None
    source_type: Optional[int] = None
    source_url: str
    search_url: Optional[str]


class SourceRequest(BaseModel):
    source_type: Optional[str] = None  # profile_source / id_source
    category_name: str  # organization / person
    jurisdiction_code: str
    client_id: str


class SourceUrlResponse(BaseModel):
    display_name: str
    source_name: str
    search_url: str
    source_url: str
