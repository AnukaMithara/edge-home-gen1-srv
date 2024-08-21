from fastapi import APIRouter, HTTPException

from app.config.database_config import db_dependency
from app.config.logging_config import get_logger
from app.model.source_model import SourceModel, SourceRequest
from app.service.source_service import SourceService

router = APIRouter(
    prefix="/v1/source",
    tags=["Source"]
)
logger = get_logger(class_name=__name__)
source_service = SourceService()


@router.post("/")
def create_source(source: SourceModel, db: db_dependency):
    return source_service.create_source(source=source, db=db)


@router.get("/{source_id}")
def get_source_by_id(source_id: int, db: db_dependency):
    source = source_service.get_source_by_id(source_id=source_id, db=db)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.get("/source_name/{source_name}")
def get_source_by_source_name(source_name: str, db: db_dependency):
    source = source_service.get_source_by_source_name(source_name=source_name, db=db)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.get("/getAll")
def get_all_sources(db: db_dependency):
    return source_service.get_all_sources(db=db)


@router.put("/{source_id}")
def update_source(source_id: int, source: SourceModel, db: db_dependency):
    return source_service.update_source(source_id=source_id, source=source, db=db)


@router.delete("/{source_id}")
def delete_source(source_id: int, db: db_dependency):
    return source_service.delete_source(source_id=source_id, db=db)


@router.post("/source-url")
async def get_url(source_url_req: SourceRequest, db: db_dependency):
    logger.info(f"Request for url {source_url_req}")
    return await source_service.get_source_url(source_url_req, db)


@router.post("/credibility")
async def get_credibility(source_credibility_req: SourceRequest, db: db_dependency):
    logger.info(f"Request for credibility {source_credibility_req}")
    return await source_service.get_source_credibility(source_credibility_req, db)
