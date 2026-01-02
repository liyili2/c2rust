from typing import Optional
from dataclasses import dataclass

@dataclass
class DeclarationInfo:
    name: Optional[str] = None
    type: Optional[str] = None
    fields: Optional[list] = None
    isUnsafe: Optional[bool] = None
    def_kind: Optional[int] = None
    visibility: Optional[str] = None
    isMutable: Optional[str] = None
    isExtern: Optional[str] = None

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value
