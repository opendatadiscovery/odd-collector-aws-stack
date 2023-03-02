from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ResourceMetadata:
    name: str
    type: str
    details: Any
