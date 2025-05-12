from dataclasses import dataclass
from datetime import datetime

@dataclass
class Link:
    url: str
    id: int = None
    created_at: datetime = None
    
    @classmethod
    def create(cls, url: str):
        return cls(url=url, created_at=datetime.utcnow())
