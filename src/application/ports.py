from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.link import Link

class LinkRepository(ABC):
    @abstractmethod
    async def save(self, link: Link) -> Link:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Link]:
        pass
    
    @abstractmethod
    async def remove(self, link_id: int) -> bool:
        pass
