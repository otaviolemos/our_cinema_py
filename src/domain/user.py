from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class User:
    username: str
    id: Optional[UUID] = None