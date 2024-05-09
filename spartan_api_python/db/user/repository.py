import uuid

from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

from spartan_api_python.db.user.table import UserEntity


class UserRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def insert(self, entity: UserEntity) -> UserEntity:
        with self.engine.connect():
            session = sessionmaker(autoflush=True, bind=self.engine)()
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    def by_id(self, id: uuid) -> UserEntity:
        with self.engine.connect():
            session = sessionmaker(autoflush=True, bind=self.engine)()
            return session.query(UserEntity).get(id)
