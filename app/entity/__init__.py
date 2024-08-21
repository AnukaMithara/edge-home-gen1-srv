from app.config.database_config import engine
from app.entity import (
    source,
    client,
    credibility,
    data_attribute,
    jurisdiction,
    jurisdiction_source,
    source_category,
    source_data_attribute_client,
    source_type,
    client_source
)

base_classes = [source.Base, client.Base, credibility.Base, data_attribute.Base, jurisdiction.Base,
                jurisdiction_source.Base, source_category.Base, source_data_attribute_client.Base,
                source_type.Base, client_source.Base]

for base_class in base_classes:
    base_class.metadata.create_all(bind=engine)
