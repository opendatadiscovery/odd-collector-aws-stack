from typing import List, Literal, Optional

from odd_collector_sdk.domain.plugin import Plugin as BasePlugin
from odd_collector_sdk.types import PluginFactory

class WithHost(BasePlugin):
    host: str


class WithPort(BasePlugin):
    port: str


class DatabasePlugin(WithHost, WithPort):
    database: Optional[str]
    user: str
    password: str

class OddAdapterPlugin(BasePlugin):
    type: Literal["odd_adapter"]
    host: str
    data_source_oddrn: str

class AwsStackPlugin(BasePlugin):
    type: Literal["aws_stack"]
    aws_access_key_id: str
    aws_secret_access_key: str
    region: str
    services: str

PLUGIN_FACTORY: PluginFactory = {
    "odd_adapter": OddAdapterPlugin,
    "aws_stack": AwsStackPlugin
}
