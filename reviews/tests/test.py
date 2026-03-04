from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from reviews.models import Review
from profiles.models import Profile


class ReviewListAPITests(APITestCase):
    def setUp(self):
        self.business1 = User.objects.create_user(username='biz1', password='Pass12345')
        self.business2 = User.objects.create_user(username='biz2', password='Pass12345')
        self.reviewer1 = User.objects.create_user(username='rev1', password='Pass12345')
        self.reviewer2 = User.objects.create_user(username='rev2', password='Pass12345')

        self.token1 = Token.objects.create(user=self.reviewer1)
        self.token2 = Token.objects.create(user=self.reviewer2)

        Review.objects.create(
            business_user=self.business1,
            reviewer=self.reviewer1,
            rating=4,
            description='Sehr professioneller Service'
        )
        Review.objects.create(
            business_user=self.business1,
            reviewer=self.reviewer2,
            rating=5,
            description='Top Qualität und schnelle Lieferung'
        )
        Review.objects.create(
            business_user=self.business2,
            reviewer=self.reviewer1,
            rating=3,
            description='Gut aber verbesserungsfähig'
        )

    def test_get_reviews_success(self):
        url = '/api/reviews/'
        resp = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(len(data), 3)

    def test_get_reviews_filter_by_business_user(self):
        url = f'/api/reviews/?business_user_id={self.business1.id}'
        resp = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(len(data), 2)
        self.assertTrue(all(r['business_user'] == self.business1.id for r in data))

    def test_get_reviews_filter_by_reviewer(self):
        url = f'/api/reviews/?reviewer_id={self.reviewer1.id}'
        resp = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(len(data), 2)
        self.assertTrue(all(r['reviewer'] == self.reviewer1.id for r in data))

    def test_get_reviews_ordering_by_rating(self):
        url = '/api/reviews/?ordering=-rating'
        resp = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # Sollten nach rating absteigend sortiert sein
        self.assertEqual(data[0]['rating'], 5)
        self.assertEqual(data[1]['rating'], 4)
        self.assertEqual(data[2]['rating'], 3)

    def test_get_reviews_unauthenticated(self):
        url = '/api/reviews/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class ReviewCreateAPITests(APITestCase):
    def setUp(self):
        self.business = User.objects.create_user(username='biz', password='Pass12345')
        self.customer = User.objects.create_user(username='cust', password='Pass12345')
        self.other_customer = User.objects.create_user(username='cust2', password='Pass12345')

        Profile.objects.create(user=self.business, type='business')
        Profile.objects.create(user=self.customer, type='customer')
        Profile.objects.create(user=self.other_customer, type='customer')

        self.customer_token = Token.objects.create(user=self.customer)
        self.other_token = Token.objects.create(user=self.other_customer)

    def test_create_review_success(self):
        url = '/api/reviews/'
        payload = {
            "business_user": self.business.id,
            "rating": 4,
            "description": "Alles war toll!"
        }
        resp = self.client.post(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.json()
        self.assertEqual(data['business_user'], self.business.id)
        self.assertEqual(data['reviewer'], self.customer.id)
        self.assertEqual(data['rating'], 4)
        self.assertEqual(data['description'], 'Alles war toll!')

    def test_create_review_duplicate_forbidden(self):
        """Customer can only leave 1 review per business user"""
        Review.objects.create(
            business_user=self.business,
            reviewer=self.customer,
            rating=5,
            description='First review'
        )
        url = '/api/reviews/'
        payload = {
            "business_user": self.business.id,
            "rating": 2,
            "description": "Second review"
        }
        resp = self.client.post(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_review_forbidden_for_business(self):
        """Business users cannot create reviews"""
        biz_token = Token.objects.create(user=self.business)
        url = '/api/reviews/'
        payload = {
            "business_user": self.customer.id,
            "rating": 4,
            "description": "Test"
        }
        resp = self.client.post(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {biz_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_review_invalid_rating(self):
        """Rating must be 1-5"""
        url = '/api/reviews/'
        payload = {
            "business_user": self.business.id,
            "rating": 10,
            "description": "Invalid"
        }
        resp = self.client.post(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)



class ReviewUpdateAPITests(APITestCase):
    def setUp(self):
        self.business = User.objects.create_user(username='biz', password='Pass12345')
        self.customer = User.objects.create_user(username='cust', password='Pass12345')
        self.other_customer = User.objects.create_user(username='cust2', password='Pass12345')

        Profile.objects.create(user=self.business, type='business')
        Profile.objects.create(user=self.customer, type='customer')
        Profile.objects.create(user=self.other_customer, type='customer')

        self.customer_token = Token.objects.create(user=self.customer)
        self.other_token = Token.objects.create(user=self.other_customer)

        self.review = Review.objects.create(
            business_user=self.business,
            reviewer=self.customer,
            rating=3,
            description='Okay service'
        )

    def test_update_review_success(self):
        """Reviewer can update their own review"""
        url = f'/api/reviews/{self.review.id}/'
        payload = {
            "rating": 5,
            "description": "Noch besser als erwartet!"
        }
        resp = self.client.patch(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(data['rating'], 5)
        self.assertEqual(data['description'], 'Noch besser als erwartet!')
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 5)

    def test_update_review_forbidden_for_others(self):
        """Other users cannot update a review"""
        url = f'/api/reviews/{self.review.id}/'
        payload = {
            "rating": 1,
            "description": "Bad"
        }
        resp = self.client.patch(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {self.other_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 3)  # unchanged

    def test_update_review_invalid_rating(self):
        """Rating validation"""
        url = f'/api/reviews/{self.review.id}/'
        payload = {"rating": 10}
        resp = self.client.patch(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_review_not_found(self):
        """404 if review doesn't exist"""
        url = '/api/reviews/99999/'
        payload = {"rating": 5}
        resp = self.client.patch(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


class ReviewDeleteAPITests(APITestCase):
    def setUp(self):
        self.business = User.objects.create_user(username='biz', password='Pass12345')
        self.customer = User.objects.create_user(username='cust', password='Pass12345')
        self.other_customer = User.objects.create_user(username='cust2', password='Pass12345')

        Profile.objects.create(user=self.business, type='business')
        Profile.objects.create(user=self.customer, type='customer')
        Profile.objects.create(user=self.other_customer, type='customer')

        self.customer_token = Token.objects.create(user=self.customer)
        self.other_token = Token.objects.create(user=self.other_customer)

        self.review = Review.objects.create(
            business_user=self.business,
            reviewer=self.customer,
            rating=4,
            description='Good service'
        )

    def test_delete_review_success(self):
        """Reviewer can delete their own review"""
        url = f'/api/reviews/{self.review.id}/'
        resp = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(pk=self.review.id).exists())

    def test_delete_review_forbidden_for_others(self):
        """Other users cannot delete a review"""
        url = f'/api/reviews/{self.review.id}/'
        resp = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.other_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Review.objects.filter(pk=self.review.id).exists())

    def test_delete_review_unauthenticated(self):
        """Unauthenticated users get 401"""
        url = f'/api/reviews/{self.review.id}/'
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_review_not_found(self):
        """404 if review doesn't exist"""
        url = '/api/reviews/99999/'
        resp = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)