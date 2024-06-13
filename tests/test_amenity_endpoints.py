from api.amenity_manager import amenity_blueprint, data_manager
import unittest
import json
from model.amenity import Amenity
from app import app


class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.data_manager = data_manager
        self.data_manager.storage = {}

    def test_create_amenity(self):
        response = self.app.post('/amenity', json={
            'name': 'Wi-Fi'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Wi-Fi', str(response.data))

    def test_get_amenities(self):
        amenity = Amenity(name='Wi-Fi')
        self.data_manager.save(amenity)
        response = self.app.get('/amenity')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Wi-Fi', str(response.data))

    def test_get_amenity(self):
        amenity = Amenity(name='Wi-Fi')
        self.data_manager.save(amenity)
        response = self.app.get(f'/amenity/{amenity.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Wi-Fi', str(response.data))

    def test_update_amenity(self):
        amenity = Amenity(name='Wi-Fi')
        self.data_manager.save(amenity)
        response = self.app.put(f'/amenity/{amenity.id}', json={
            'name': 'High-speed Wi-Fi'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('High-speed Wi-Fi', str(response.data))

    def test_delete_amenity(self):
        amenity = Amenity(name='Wi-Fi')
        self.data_manager.save(amenity)
        response = self.app.delete(f'/amenity/{amenity.id}')
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(self.data_manager.get(amenity.id, 'Amenity'))


if __name__ == "__main__":
    unittest.main()
