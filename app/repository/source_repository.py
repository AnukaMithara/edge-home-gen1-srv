from sqlalchemy import or_
from sqlalchemy.orm import aliased

from app.entity.client import Client
from app.entity.client_source import ClientSource
from app.entity.credibility import Credibility
from app.entity.data_attribute import DataAttribute
from app.entity.jurisdiction import Jurisdiction
from app.entity.jurisdiction_source import JurisdictionSource
from app.entity.source import Source
from app.entity.source_category import SourceCategory
from app.entity.source_data_attribute_client import SourceDataAttributeClient
from app.entity.source_type import SourceType
from app.exceptions.DbOperationException import DbOperationException


class SourceRepository:
    @classmethod
    def save(cls, source, db):
        try:
            db.add(source)
            db.commit()
            db.refresh(source)
            return source
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    def get_by_id(cls, _id, db):
        try:
            source = db.query(Source).filter(Source.id == _id).first()
            return source
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    def get_by_source_name(cls, source_name, db):
        try:
            source = db.query(Source).filter(Source.source_name == source_name).first()
            return source
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    def get_all(cls, db):
        try:
            all_sources = db.query(Source).all()
            return all_sources
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    def delete(cls, _id, db):
        try:
            source = db.query(Source).filter(Source.id == _id).first()
            if source:
                source.is_active = False
                db.commit()
                return {"message": "Source removed successfully"}
            else:
                return {"message": "Not found"}
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    async def get_source(cls, request, db):
        query = db.query(Source).join(JurisdictionSource, Source.id == JurisdictionSource.source) \
            .join(Jurisdiction, JurisdictionSource.jurisdiction == Jurisdiction.id) \
            .join(ClientSource, Source.id == ClientSource.source) \
            .join(Client, Client.id == ClientSource.client) \
            .join(SourceCategory, Source.source_category == SourceCategory.id) \
            .filter(or_(Jurisdiction.jurisdiction_code == request.jurisdiction_code,
                        Jurisdiction.jurisdiction_code == "ALL",
                        Jurisdiction.jurisdiction_code == "ANY"),
                    Client.client_id == request.client_id,
                    SourceCategory.category_name == request.category_name)

        if request.source_type:
            query = query.join(SourceType, Source.source_type == SourceType.id) \
                .filter(SourceType.source_type == request.source_type)

        sources = query.all()
        return sources

    @classmethod
    async def get_credibility(cls, request, db):
        credibility_attr_alias = aliased(Credibility)
        credibility_source_alias = aliased(Credibility)
        query = (db.query(Source.source_name, credibility_source_alias.credibility, DataAttribute.attribute_name,
                          credibility_attr_alias.credibility)
                 .join(ClientSource, ClientSource.source == Source.id)
                 .join(Client, Client.id == ClientSource.client)
                 .join(JurisdictionSource, Source.id == JurisdictionSource.source)
                 .join(Jurisdiction, JurisdictionSource.jurisdiction == Jurisdiction.id)
                 .join(SourceCategory, Source.source_category == SourceCategory.id)
                 .join(SourceDataAttributeClient, SourceDataAttributeClient.client_source == ClientSource.id)
                 .join(DataAttribute, DataAttribute.id == SourceDataAttributeClient.data_attribute)
                 .join(credibility_attr_alias, credibility_attr_alias.id == SourceDataAttributeClient.credibility)
                 .join(credibility_source_alias, credibility_source_alias.id == Source.credibility)
                 .filter(or_(Jurisdiction.jurisdiction_code == request.jurisdiction_code,
                             Jurisdiction.jurisdiction_code == "ALL",
                             Jurisdiction.jurisdiction_code == "ANY"),
                         Client.client_id == request.client_id,
                         SourceCategory.category_name == request.category_name))

        if request.source_type:
            query = query.join(SourceType, Source.source_type == SourceType.id) \
                .filter(SourceType.source_type == request.source_type)

        client_sources = query.all()
        return client_sources
