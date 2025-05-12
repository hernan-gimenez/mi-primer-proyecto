from fastapi import Depends
from sqlalchemy.orm import Session

from src.domain.link import Link
from src.application.ports import LinkRepository
from src.infrastructure.database.database import LinkModel, get_db

class SQLiteLinkRepository(LinkRepository):
    def __init__(self, db: Session):
        self.db = db
    
    async def save(self, link: Link) -> Link:
        db_link = LinkModel(url=link.url, created_at=link.created_at)
        self.db.add(db_link)
        self.db.commit()
        self.db.refresh(db_link)
        link.id = db_link.id
        return link
    
    async def get_all(self) -> list[Link]:
        db_links = self.db.query(LinkModel).all()
        return [
            Link(
                id=db_link.id,
                url=db_link.url,
                created_at=db_link.created_at
            ) for db_link in db_links
        ]
    
    async def remove(self, link_id: int) -> bool:
        db_link = self.db.query(LinkModel).filter(LinkModel.id == link_id).first()
        if not db_link:
            return False
        self.db.delete(db_link)
        self.db.commit()
        return True

def get_link_repository(db: Session = Depends(get_db)) -> LinkRepository:
    return SQLiteLinkRepository(db)
