import contextlib
import logging
from abc import ABC, abstractmethod
import os

from odd_collector.adapters.aws_stack.exceptions import AWSConnectionException
from subprocess import call

class AbstractConnector(ABC):  # TODO: Create one abstract connector for all adapters
    @abstractmethod
    def connection(self):
        pass


class AWSStackConnector(AbstractConnector):
    __filename = ''

    def __init__(self, config) -> None:
        self.__aws_access_key_id = config.aws_access_key_id
        self.__aws_secret_access_key = config.aws_secret_access_key
        self.__region = config.region
        self.__services = config.services
        self.connection()

    def get_filename(self):
        return self.__filename

    @contextlib.contextmanager
    def connection(self):
        self.__connect()
    
    def disconnection(self):
        self.__disconnect()
    
    def __generate_filename(self):
        import random
        import string
        self.__filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + '.yml'

    def __connect(self):
        try:
            self.__generate_filename()
            os.environ['AWS_ACCESS_KEY_ID'] = self.__aws_access_key_id
            os.environ['AWS_SECRET_ACCESS_KEY'] = self.__aws_secret_access_key
            call(['aws', 'ecr', 'get-login', '--region', self.__region])

            call(['former2', 'generate', 
                '--output-cloudformation', './ymls/'+self.__filename, 
                '--services', self.__services, 
                '--region', self.__region])
            
        except Exception as e:
            logging.debug("Error in __connect method", exc_info=True)
            raise AWSConnectionException(
                "Cannot connect to AWS. Check if keys have sufficient permissions", str(e)
            ) from e

    def __disconnect(self):
        call(['rm', './'+self.__filename])