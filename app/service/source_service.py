from collections import defaultdict

from app.entity.source import Source
from app.model.source_model import SourceModel, SourceUrlResponse
from app.repository.source_repository import SourceRepository
from app.service.http_service import logger
from app.util.generic_response import GenericResponse

from audit_log_gen1_mod.app.service.audit_service import AuditService

audit_service = AuditService()

from app.config.audit_config import CLIENT_ID, TENANT_ID, USER


class SourceService:
    @classmethod
    def create_source(cls, source: SourceModel, db):
        try:
            logger.info("Create Source Process Started")
            new_source = Source(
                source_name=source.source_name,
                display_name=source.display_name,
                source_category=source.source_category,
                source_type=source.source_type,
                source_url=source.source_url,
                search_url=source.search_url,
                credibility=source.credibility
            )
            saved_source = SourceRepository.save(new_source, db)

            try:
                audit_service.create_audit(
                    client_id=CLIENT_ID,
                    tenant_id=TENANT_ID,
                    process_name="Create Source",
                    action="Create",
                    message=f"User {USER} Created a new Source {source.source_name}",
                    metadata=saved_source,
                    service_name="Source Service",
                    identifier=str(source.source_name),
                )
                logger.info("Audit Log Created Successfully")
            except Exception as ex:
                logger.error(f"Audit Log Creation Error: {str(ex)}")

            logger.info("Create Source Process End")
            return GenericResponse.success(message="Create Project Source Success", results=saved_source)
        except Exception as ex:
            logger.error(f"Create Source Error: {str(ex)}")
            logger.info("Create Source End With Error")
            return GenericResponse.failed(message=f"Create Source Failed, Error: {str(ex)}", results=[])

    @classmethod
    def get_source_by_id(cls, source_id: int, db):
        try:
            logger.info("Get Source by id Process Started")
            source = SourceRepository.get_by_id(source_id, db)

            try:
                audit_service.create_audit(
                    client_id=CLIENT_ID,
                    tenant_id=TENANT_ID,
                    process_name="Get Source by id",
                    action="Get",
                    message=f"User {USER} fetched Source {source.source_name}",
                    metadata={},
                    service_name="Source Service",
                    identifier=str(source_id),
                )
                logger.info("Audit Log Created Successfully")
            except Exception as ex:
                logger.error(f"Audit Log Creation Error: {str(ex)}")

            logger.info("Get Source by id Process End")
            return GenericResponse.success(message="Get Source Success", results=source)
        except Exception as ex:
            logger.error(f"Get Source Error: {str(ex)}")
            logger.info("Get Source End With Error")
            return GenericResponse.failed(message=f"Get Source Failed, Error: {str(ex)}", results=[])

    @classmethod
    def get_source_by_source_name(cls, source_name: str, db):
        try:
            logger.info("Get Source by source_name Process Started")
            source = SourceRepository.get_by_source_name(source_name, db)

            try:
                audit_service.create_audit(
                    client_id=CLIENT_ID,
                    tenant_id=TENANT_ID,
                    process_name="Get Source by source_name",
                    action="Get",
                    message=f"User {USER} fetched Source {source.source_name}",
                    metadata={},
                    service_name="Source Service",
                    identifier=str(source_name),
                )
                logger.info("Audit Log Created Successfully")
            except Exception as ex:
                logger.error(f"Audit Log Creation Error: {str(ex)}")

            logger.info("Get Source by source_name Process End")
            return GenericResponse.success(message="Get Source Success", results=source)
        except Exception as ex:
            logger.info("Get Source by source_name Process End With Error")
            logger.error(f"Get Source Error: {str(ex)}")
            return GenericResponse.failed(message=f"Get Source Failed, Error: {str(ex)}", results=[])

    @classmethod
    def get_all_sources(cls, db):
        try:
            logger.info("Get All Sources Process Started")
            source_details = SourceRepository.get_all(db)

            try:
                audit_service.create_audit(
                    client_id=CLIENT_ID,
                    tenant_id=TENANT_ID,
                    process_name="Get All Sources",
                    action="Get",
                    message=f"User {USER} fetched all Sources",
                    metadata={},
                    service_name="Source Service",
                    identifier="All Sources",
                )
                logger.info("Audit Log Created Successfully")
            except Exception as ex:
                logger.error(f"Audit Log Creation Error: {str(ex)}")

            logger.info("Get All Sources Process End")
            return GenericResponse.success(message="Get All Sources Success", results=source_details)
        except Exception as ex:
            logger.info("Get All Sources Process End With Error")
            logger.error(f"Get All Sources Error: {str(ex)}")
            return GenericResponse.failed(message=f"Get All Sources Failed, Error: {str(ex)}", results=[])

    @classmethod
    def update_source(cls, source_id: int, source: SourceModel, db):
        try:
            logger.info("Update Source Process Started")
            existing_source = SourceRepository.get_by_id(source_id, db)

            existing_source.source_name = source.source_name
            existing_source.display_name = source.display_name
            existing_source.source_category = source.source_category
            existing_source.source_type = source.source_type
            existing_source.source_url = source.source_url
            existing_source.search_url = source.search_url

            updated_source = SourceRepository.save(existing_source, db)

            try:
                audit_service.create_audit(
                    client_id=CLIENT_ID,
                    tenant_id=TENANT_ID,
                    process_name="Update Source",
                    action="Update",
                    message=f"User {USER} updated Source {source.source_name}",
                    metadata=updated_source,
                    service_name="Source Service",
                    identifier=str(source_id),
                )
                logger.info("Audit Log Created Successfully")
            except Exception as ex:
                logger.error(f"Audit Log Creation Error: {str(ex)}")

            logger.info("Update Source Process End")
            return GenericResponse.success(message="Update Source Success", results=updated_source)
        except Exception as ex:
            logger.info("Update Source Process End With Error")
            logger.error(f"Update Source Error: {str(ex)}")
            return GenericResponse.failed(message=f"Update Source Failed, Error: {str(ex)}", results=[])

    @classmethod
    def delete_source(cls, source_id: int, db):
        try:
            logger.info("Delete Source Process Started")
            source = SourceRepository.get_by_id(source_id, db)
            deleted_source = SourceRepository.delete(source_id, db)

            try:
                audit_service.create_audit(
                    client_id=CLIENT_ID,
                    tenant_id=TENANT_ID,
                    process_name="Delete Source",
                    action="Delete",
                    message=f"User {USER} deleted Source {source.source_name}",
                    metadata=source,
                    service_name="Source Service",
                    identifier=str(source_id),
                )
                logger.info("Audit Log Created Successfully")
            except Exception as ex:
                logger.error(f"Audit Log Creation Error: {str(ex)}")

            logger.info("Delete Source Process End")
            return GenericResponse.success(message="Delete Source Success", results=deleted_source)
        except Exception as ex:
            logger.info("Delete Source Process End With Error")
            logger.error(f"Delete Source Error: {str(ex)}")
            return GenericResponse.failed(message=f"Delete Source Failed, Error: {str(ex)}", results=[])

    @classmethod
    async def get_source_url(cls, source_url_req, db):
        source_urls = await SourceRepository.get_source(source_url_req, db)
        source_urls_res = []
        for source_url in source_urls:
            source_url_res = SourceUrlResponse(display_name=source_url.display_name,
                                               source_name=source_url.source_name,
                                               source_url=source_url.source_url,
                                               search_url=source_url.search_url)
            source_urls_res.append(source_url_res)

        try:
            audit_service.create_audit(
                client_id=CLIENT_ID,
                tenant_id=TENANT_ID,
                process_name="Get Source URL",
                action="Get",
                message=f"User {USER} fetched Source URLs",
                metadata={},
                service_name="Source Service",
                identifier="All Sources",
            )
            logger.info("Audit Log Created Successfully")
        except Exception as ex:
            logger.error(f"Audit Log Creation Error: {str(ex)}")

        return GenericResponse.success(message="Get source url success", results=source_urls_res)

    @classmethod
    async def get_source_credibility(cls, source_credibility_req, db):
        credibility = await SourceRepository.get_credibility(source_credibility_req, db)
        attr_credibility_list = defaultdict(dict)
        for source_name, source_credibility, attribute_name, attr_credibility in credibility:
            attr_credibility_list[attribute_name][source_name] = attr_credibility

        sources = await SourceRepository.get_source(source_credibility_req, db)
        source_list = {}
        for source in sources:
            source_list[source.source_name] = {"display_name": source.display_name,
                                               "source_url": source.source_url,
                                               "search_url": source.search_url,
                                               "credibility": source.credibility}

        try:
            audit_service.create_audit(
                client_id=CLIENT_ID,
                tenant_id=TENANT_ID,
                process_name="Get Source Credibility",
                action="Get",
                message=f"User {USER} fetched Source Credibility",
                metadata={},
                service_name="Source Service",
                identifier="All Sources",
            )
            logger.info("Audit Log Created Successfully")
        except Exception as ex:
            logger.error(f"Audit Log Creation Error: {str(ex)}")

        return GenericResponse.success(message="Get source credibility success",
                                       results={
                                           "sources": source_list,
                                           "credibility": attr_credibility_list
                                       })
