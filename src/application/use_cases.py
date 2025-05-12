from typing import List
from datetime import datetime

from src.domain.link import Link
from src.application.ports import LinkRepository

class LinkService:
    def __init__(self, link_repository: LinkRepository):
        self.link_repository = link_repository
    
    async def create_link(self, url: str) -> Link:
        link = Link.create(url)
        return await self.link_repository.save(link)
    
    async def list_links(self) -> List[Link]:
        return await self.link_repository.get_all()
    
    async def remove_link(self, link_id: int) -> bool:
        return await self.link_repository.remove(link_id)
