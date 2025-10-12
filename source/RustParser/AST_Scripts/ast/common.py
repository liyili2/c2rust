from typing import Optional
from dataclasses import dataclass

@dataclass
class DeclarationInfo:
    name: str
    type: Optional[str] = None
    visibility: Optional[str] = None
