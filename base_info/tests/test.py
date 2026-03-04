from rest_framework.test import APITestCase


class BaseInfoAPITest(APITestCase):
    def test_get_base_info_returns_expected_keys(self):
        resp = self.client.get('/api/base-info/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        for key in ('review_count', 'average_rating', 'business_profile_count', 'offer_count'):
            self.assertIn(key, data)
        self.assertIsInstance(data['review_count'], int)
        # average_rating may be int/float, coerce check
        self.assertTrue(isinstance(data['average_rating'], (int, float)))
        self.assertIsInstance(data['business_profile_count'], int)
        self.assertIsInstance(data['offer_count'], int)