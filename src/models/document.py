from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Document:
    text: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}