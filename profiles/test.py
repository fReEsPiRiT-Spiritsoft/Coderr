from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from profiles.models import Profile

class ProfileAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='profuser', email='prof@example.com', password='Pass12345'
        )
        # Erstelle ein aussagekräftiges Profile-Objekt (felder laut Spec)
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='Max',
            last_name='Mustermann',
            location='Berlin',
            tel='123456789',
            description='Business description',
            working_hours='9-17',
            type='business'
        )
        self.token = Token.objects.create(user=self.user)

    def test_get_profile_success(self):
        url = f'/api/profile/{self.user.id}/'
        resp = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(data.get('user'), self.user.id)
        self.assertEqual(data.get('username'), self.user.username)
        self.assertEqual(data.get('email'), self.user.email)
        self.assertEqual(data.get('first_name'), 'Max')


    def test_get_profile_unauthenticated(self):
        url = f'/api/profile/{self.user.id}/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_not_found(self):
        url = f'/api/profile/999999/'
        resp = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_profile_success(self):
        url = f'/api/profile/{self.user.id}/'
        payload = {
            "first_name": "Updated",
            "last_name": "User",
            "location": "Munich",
            "tel": "000111222",
            "description": "Updated business description",
            "working_hours": "8-16",
            "email": "newemail@example.com"
        }
        resp = self.client.patch(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(data.get('first_name'), "Updated")
        self.assertEqual(data.get('last_name'), "User")
        self.assertEqual(data.get('location'), "Munich")
        self.assertEqual(data.get('tel'), "000111222")
        self.assertEqual(data.get('description'), "Updated business description")
        self.assertEqual(data.get('working_hours'), "8-16")
        # email is proxied to user.email via serializer's source='user.email'
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "newemail@example.com")

    def test_patch_profile_forbidden_for_non_owner(self):
        other = User.objects.create_user(username='other', email='o@example.com', password='Pass12345')
        other_token = Token.objects.create(user=other)
        url = f'/api/profile/{self.user.id}/'
        payload = {"first_name": "Hacker"}
        resp = self.client.patch(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {other_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_profile_unauthenticated(self):
        url = f'/api/profile/{self.user.id}/'
        payload = {"first_name": "ShouldFail"}
        resp = self.client.patch(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)