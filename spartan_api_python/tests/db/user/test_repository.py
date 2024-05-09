import unittest

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from spartan_api_python.db.user.repository import UserRepository
from spartan_api_python.db.user.table import UserEntity


class UserRepositoryTest(unittest.TestCase):
    engine = create_engine("postgresql://local:local@localhost:5432/local")
    repository: UserRepository

    def setUp(self):
        with self.engine.connect():
            session = self.session(self.engine)
            session.query(UserEntity).delete()
            self.repository = UserRepository(self.engine)

    def tearDown(self):
        pass

    def test_insert(self):
        entity = UserEntity(
            email="",
            status="active",
            level="user",
            phone="+18186264197"
        )
        result = self.repository.insert(entity=entity)
        self.assertEqual(result.email, entity.email)
        self.assertEqual(result.status, entity.status)
        self.assertEqual(result.phone, entity.phone)

    def test_by_id(self):
        entity = UserEntity(
            email="",
            status="active",
            level="user",
            phone="+18186264197"
        )
        result = self.repository.insert(entity=entity)
        after = self.repository.by_id(result.id)
        self.assertEqual(after.email, entity.email)
        self.assertEqual(after.status, entity.status)
        self.assertEqual(after.phone, entity.phone)

    @staticmethod
    def session(engine: Engine) -> Session:
        return sessionmaker(autoflush=True, bind=engine)()
