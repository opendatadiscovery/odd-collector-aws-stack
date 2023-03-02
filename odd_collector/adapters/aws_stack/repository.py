from abc import ABC, abstractmethod
from typing import List, Union
import yaml
from cfn_tools import load_yaml, dump_yaml
import logging
from odict import odict

from odd_collector.adapters.aws_stack.connectors import AWSStackConnector


class AbstractRepository(ABC):
    @abstractmethod
    def get_resources(self):
        pass

class AWSStackRepository(AbstractRepository):
    def __init__(self, config):
        self.__aws_stack_connector = AWSStackConnector(config)
        text = open('./ymls/'+self.__aws_stack_connector.get_filename()).read()
        self.__data = load_yaml(text)['Resources']

    def get_resources(self) -> List[odict]:
        return self.__data