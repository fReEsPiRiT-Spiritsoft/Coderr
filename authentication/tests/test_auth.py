from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class AuthTests(APITestCase):
    def test_registration_success(self):
        payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "StrongPass123",
            "repeated_password": "StrongPass123",
            "type": "customer"
        }
        resp = self.client.post('/api/registration/', payload, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertIn('token', resp.data)
        self.assertEqual(resp.data['username'], payload['username'])
        self.assertEqual(resp.data['email'], payload['email'])
        self.assertIn('user_id', resp.data)
        self.assertTrue(User.objects.filter(username=payload['username']).exists())
        user = User.objects.get(username=payload['username'])
        self.assertTrue(Token.objects.filter(user=user).exists())

    def test_registration_password_mismatch(self):
        payload = {
            "username": "baduser",
            "email": "bad@example.com",
            "password": "pass1",
            "repeated_password": "pass2",
            "type": "customer"
        }
        resp = self.client.post('/api/registration/', payload, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_login_success(self):
        user = User.objects.create_user(username='loginuser', email='li@example.com', password='LoginPass123')
        resp = self.client.post('/api/login/', {"username": "loginuser", "password": "LoginPass123"}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('token', resp.data)
        self.assertEqual(resp.data['username'], 'loginuser')
        self.assertEqual(resp.data['email'], 'li@example.com')
        # token from response must match stored token
        token = Token.objects.get(user=user)
        self.assertEqual(resp.data['token'], token.key)

    def test_login_invalid_credentials(self):
        resp = self.client.post('/api/login/', {"username": "nope", "password": "wrong"}, format='json')
        self.assertEqual(resp.status_code, 400)