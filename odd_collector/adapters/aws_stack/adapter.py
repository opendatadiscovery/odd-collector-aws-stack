import logging
from typing import List

from odd_collector_sdk.domain.adapter import AbstractAdapter
from odd_models.models import DataEntity, DataEntityList
from oddrn_generator import PostgresqlGenerator

from .logger import logger
from .mappers.tables import map_table
from .repository import AWSStackRepository


class Adapter(AbstractAdapter):
    def __init__(self, config) -> None:
        self.__database = config.description
        self.__repository = AWSStackRepository(config)
        self.__oddrn_generator = PostgresqlGenerator(
            host_settings=f"aws_stack_{config.aws_access_key_id}", databases=self.__database
        )

    def get_data_source_oddrn(self) -> str:
        return self.__oddrn_generator.get_data_source_oddrn()

    def get_data_entities(self) -> List[DataEntity]:
        try:
            resources = self.__repository.get_resources()
            #details = self.__repository.get_details()
            #resource_types = self.__repository.get_resource_types()

            return map_table(
                self.__oddrn_generator, resources, self.__database
            )
        except Exception:
            logger.error("Failed to load metadata for resources", exc_info=True)
            return []

    def get_data_entity_list(self) -> DataEntityList:
        return DataEntityList(
            data_source_oddrn=self.get_data_source_oddrn(),
            items=(self.get_data_entities()),
        )
