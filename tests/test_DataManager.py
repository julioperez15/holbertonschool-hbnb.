import unittest
from model.user import User
from persistence.DataManager import DataManager


class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.user = User(email="test@example.com", password="password")

    def test_save_and_get(self):
        self.data_manager.save(self.user)
        retrieved_user = self.data_manager.get(self.user.id, 'User')
        self.assertEqual(retrieved_user.email, "test@example.com")

    def test_update(self):
        self.data_manager.save(self.user)
        self.user.first_name = "Test"
        self.data_manager.update(self.user)
        retrieved_user = self.data_manager.get(self.user.id, 'User')
        self.assertEqual(retrieved_user.first_name, "Test")

    def test_delete(self):
        self.data_manager.save(self.user)
        self.data_manager.delete(self.user.id, 'User')
        retrieved_user = self.data_manager.get(self.user.id, 'User')
        self.assertIsNone(retrieved_user)


if __name__ == "__main__":
    unittest.main()