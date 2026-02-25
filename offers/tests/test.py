from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from offers.models import Offer, OfferDetail
from profiles.models import Profile

class OffersAPITests(APITestCase):
    def setUp(self):
        # users
        self.business_user = User.objects.create_user(
            username='biz', email='biz@example.com', password='Pass12345'
        )
        self.customer_user = User.objects.create_user(
            username='cust', email='cust@example.com', password='Pass12345'
        )

        # profiles
        Profile.objects.create(user=self.business_user, type='business')
        Profile.objects.create(user=self.customer_user, type='customer')

        # tokens
        self.business_token = Token.objects.create(user=self.business_user)
        self.customer_token = Token.objects.create(user=self.customer_user)

        # an offer by business user
        self.offer = Offer.objects.create(
            user=self.business_user,
            title='Website Design',
            description='Professional website design',
            min_price=100.00,
            min_delivery_time=7
        )
        OfferDetail.objects.create(offer=self.offer, url='http://example.com/detail/1')

    def test_get_offers_list(self):
        url = '/api/offers/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # pagination -> results present
        self.assertIn('results', data)
        results = data['results']
        self.assertTrue(len(results) >= 1)
        first = results[0]
        self.assertEqual(first.get('id'), self.offer.id)
        self.assertEqual(first.get('title'), 'Website Design')
        self.assertIn('user_details', first)
        self.assertIn('details', first)
        self.assertIsInstance(first['details'], list)

    def test_post_offer_success_business_user(self):
        url = '/api/offers/'
        payload = {
            "title": "Graphicpack",
            "description": "Comprehensive graphics package",
            "min_price": 200.0,
            "min_delivery_time": 5,
            "details": [
                {"url": "http://example.com/d1"},
                {"url": "http://example.com/d2"}
            ]
        }
        resp = self.client.post(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {self.business_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # DB objects created
        offer = Offer.objects.filter(title='Graphicpack').first()
        self.assertIsNotNone(offer)
        self.assertEqual(OfferDetail.objects.filter(offer=offer).count(), 2)

    def test_post_offer_forbidden_for_non_business(self):
        url = '/api/offers/'
        payload = {
            "title": "Should Fail",
            "description": "No rights",
            "min_price": 10.0,
            "min_delivery_time": 1,
            "details": []
        }
        resp = self.client.post(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_offer_unauthenticated(self):
        url = '/api/offers/'
        payload = {
            "title": "NoAuth",
            "description": "No auth",
            "min_price": 1.0,
            "min_delivery_time": 1
        }
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
# filepath: /home/patricks/Schreibtisch/Developer Academie/!Backend-Kurs/Coderr/offers/tests/test.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from offers.models import Offer, OfferDetail
from profiles.models import Profile

class OffersAPITests(APITestCase):
    def setUp(self):
        # users
        self.business_user = User.objects.create_user(
            username='biz', email='biz@example.com', password='Pass12345'
        )
        self.customer_user = User.objects.create_user(
            username='cust', email='cust@example.com', password='Pass12345'
        )

        # profiles
        Profile.objects.create(user=self.business_user, type='business')
        Profile.objects.create(user=self.customer_user, type='customer')

        # tokens
        self.business_token = Token.objects.create(user=self.business_user)
        self.customer_token = Token.objects.create(user=self.customer_user)

        # an offer by business user
        self.offer = Offer.objects.create(
            user=self.business_user,
            title='Website Design',
            description='Professional website design',
            min_price=100.00,
            min_delivery_time=7
        )
        OfferDetail.objects.create(offer=self.offer, url='http://example.com/detail/1')

    def test_get_offers_list(self):
        url = '/api/offers/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # pagination -> results present
        self.assertIn('results', data)
        results = data['results']
        self.assertTrue(len(results) >= 1)
        first = results[0]
        self.assertEqual(first.get('id'), self.offer.id)
        self.assertEqual(first.get('title'), 'Website Design')
        self.assertIn('user_details', first)
        self.assertIn('details', first)
        self.assertIsInstance(first['details'], list)

    def test_post_offer_success_business_user(self):
        url = '/api/offers/'
        payload = {
            "title": "Graphicpack",
            "description": "Comprehensive graphics package",
            "min_price": 200.0,
            "min_delivery_time": 5,
            "details": [
                {"url": "http://example.com/d1"},
                {"url": "http://example.com/d2"}
            ]
        }
        resp = self.client.post(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {self.business_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # DB objects created
        offer = Offer.objects.filter(title='Graphicpack').first()
        self.assertIsNotNone(offer)
        self.assertEqual(OfferDetail.objects.filter(offer=offer).count(), 2)

    def test_post_offer_forbidden_for_non_business(self):
        url = '/api/offers/'
        payload = {
            "title": "Should Fail",
            "description": "No rights",
            "min_price": 10.0,
            "min_delivery_time": 1,
            "details": []
        }
        resp = self.client.post(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_offer_unauthenticated(self):
        url = '/api/offers/'
        payload = {
            "title": "NoAuth",
            "description": "No auth",
            "min_price": 1.0,
            "min_delivery_time": 1
        }
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)