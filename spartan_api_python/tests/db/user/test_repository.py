import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from spartan_api_python.db.user.repository import UserRepository
from spartan_api_python.db.user.table import UserTable


class UserRepositoryTest(unittest.TestCase):
    engine = create_engine("postgresql://local:local@localhost:5432/local")
    repository: UserRepository

    def setUp(self):
        session = self.session()
        session.query(UserTable).delete()
        self.repository = UserRepository(session=session)
        self.engine.connect()
        pass

    def tearDown(self):
        pass

    def test_insert(self):
        entity = UserTable(
            email="",
            status="active",
            level="user",
            phone="+18186264197"
        )
        result = self.repository.insert(entity=entity)
        self.assertEqual(result.email, entity.email)
        self.assertEqual(result.status, entity.status)
        self.assertEqual(result.phone, entity.phone)

    def session(self) -> Session:
        return sessionmaker(autoflush=True, bind=self.engine)()
