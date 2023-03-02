import logging
from typing import List
from odict import odict

from odd_models.models import DataEntity, DataEntityGroup, DataSet
from oddrn_generator import PostgresqlGenerator

from odd_collector.adapters.postgresql.config import (
    _data_set_metadata_excluded_keys,
    _data_set_metadata_schema_url,
)

from ..exceptions import MappingException
from .metadata import append_metadata_extension
from .models import ResourceMetadata
from .types import RESOURCE_TYPES_AWS_TO_ODD, DataEntityType
from .views import extract_transformer_data


def map_table(
    oddrn_generator: PostgresqlGenerator,
    resources: List[tuple],
    database: str,
) -> List[DataEntity]:
    data_entities: List[DataEntity] = []
    column_index: int = 0

    for key, resource in resources.items():
        try:
            resource: odict = odict(resource) 

            data_entity_type = RESOURCE_TYPES_AWS_TO_ODD.get(
                resource.values()[0], DataEntityType.UNKNOWN
            )
            oddrn_path = str(data_entity_type)

            logging.error(key)

            oddrn_generator.set_oddrn_paths(
                **{"schemas": "hello", oddrn_path: str(key)}
            )

            # DataEntity
            data_entity: DataEntity = DataEntity(
                oddrn=oddrn_generator.get_oddrn_by_path(oddrn_path),
                name=key,
                type=data_entity_type,
                metadata=[],
            )
            data_entities.append(data_entity)
        except Exception as err:
            logging.error("Error in map_table", exc_info=True)
            raise MappingException(err) from err

    return data_entities
