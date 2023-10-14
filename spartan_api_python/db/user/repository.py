import uuid

from sqlalchemy.orm import Session

from spartan_api_python.db.user.table import UserTable


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def insert(self, entity: UserTable) -> UserTable:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def by_id(self, id: uuid) -> UserTable:
        return self.session.query(UserTable).get(id)
