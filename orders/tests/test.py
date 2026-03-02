from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from orders.models import Order
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from offers.models import Offer, OfferDetail
from profiles.models import Profile


class OrderAPITests(APITestCase):
    def setUp(self):
        # Create users
        self.customer = User.objects.create_user(
            username='customer1', email='cust@example.com', password='Pass12345'
        )
        self.business = User.objects.create_user(
            username='business1', email='biz@example.com', password='Pass12345'
        )
        self.other_user = User.objects.create_user(
            username='other', email='other@example.com', password='Pass12345'
        )

        # Create tokens
        self.customer_token = Token.objects.create(user=self.customer)
        self.business_token = Token.objects.create(user=self.business)
        self.other_token = Token.objects.create(user=self.other_user)

        # Create orders
        self.order1 = Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title='Logo Design',
            revisions=3,
            delivery_time_in_days=5,
            price=150.00,
            features=['Logo Design', 'Visitenkarten'],
            offer_type='basic',
            status='in_progress'
        )
        self.order2 = Order.objects.create(
            customer_user=self.customer,
            business_user=self.other_user,
            title='Website Design',
            revisions=2,
            delivery_time_in_days=10,
            price=500.00,
            features=['Website Design', 'Hosting'],
            offer_type='standard',
            status='pending'
        )

    def test_get_orders_as_customer(self):from rest_framework.test import APITestCase



class OrderAPITests(APITestCase):
    def setUp(self):
        # Create users
        self.customer = User.objects.create_user(
            username='customer1', email='cust@example.com', password='Pass12345'
        )
        self.business = User.objects.create_user(
            username='business1', email='biz@example.com', password='Pass12345'
        )
        self.other_user = User.objects.create_user(
            username='other', email='other@example.com', password='Pass12345'
        )

        # Create tokens
        self.customer_token = Token.objects.create(user=self.customer)
        self.business_token = Token.objects.create(user=self.business)
        self.other_token = Token.objects.create(user=self.other_user)

        # Create orders
        self.order1 = Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title='Logo Design',
            revisions=3,
            delivery_time_in_days=5,
            price=150.00,
            features=['Logo Design', 'Visitenkarten'],
            offer_type='basic',
            status='in_progress'
        )
        self.order2 = Order.objects.create(
            customer_user=self.customer,
            business_user=self.other_user,
            title='Website Design',
            revisions=2,
            delivery_time_in_days=10,
            price=500.00,
            features=['Website Design', 'Hosting'],
            offer_type='standard',
            status='pending'
        )

    def test_get_orders_as_customer(self):
        """Customer should see orders they created"""
        url = '/api/orders/'
        resp = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # customer should see both orders they are involved in
        self.assertEqual(len(data), 2)
        order_ids = [o['id'] for o in data]
        self.assertIn(self.order1.id, order_ids)
        self.assertIn(self.order2.id, order_ids)

    def test_get_orders_as_business(self):
        """Business user should see orders they are assigned to"""
        url = '/api/orders/'
        resp = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.business_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # business should see only order1 (where they are business_user)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], self.order1.id)
        self.assertEqual(data[0]['title'], 'Logo Design')
        self.assertEqual(data[0]['status'], 'in_progress')

    def test_get_orders_unauthenticated(self):
        """Unauthenticated users should get 401"""
        url = '/api/orders/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_orders_other_user_no_access(self):
        """User without involvement should see empty list"""
        # Create a user with no orders
        new_user = User.objects.create_user(username='newuser', email='new@example.com', password='Pass12345')
        new_token = Token.objects.create(user=new_user)
        url = '/api/orders/'
        resp = self.client.get(url, HTTP_AUTHORIZATION=f'Token {new_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(len(data), 0)
        """Customer should see orders they created"""
        url = '/api/orders/'
        resp = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # customer should see both orders they are involved in
        self.assertEqual(len(data), 2)
        order_ids = [o['id'] for o in data]
        self.assertIn(self.order1.id, order_ids)
        self.assertIn(self.order2.id, order_ids)

    def test_get_orders_as_business(self):
        """Business user should see orders they are assigned to"""
        url = '/api/orders/'
        resp = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.business_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # business should see only order1 (where they are business_user)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], self.order1.id)
        self.assertEqual(data[0]['title'], 'Logo Design')
        self.assertEqual(data[0]['status'], 'in_progress')

    def test_get_orders_unauthenticated(self):
        """Unauthenticated users should get 401"""
        url = '/api/orders/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_orders_other_user_no_access(self):
        """User without involvement should see empty list"""
        # Create a user with no orders
        new_user = User.objects.create_user(username='newuser', email='new@example.com', password='Pass12345')
        new_token = Token.objects.create(user=new_user)
        url = '/api/orders/'
        resp = self.client.get(url, HTTP_AUTHORIZATION=f'Token {new_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(len(data), 0)

class OrderCreateAPITests(APITestCase):
    def setUp(self):
        # Nutzer und Profile
        self.customer = User.objects.create_user(username='customer', password='Pass12345')
        self.business = User.objects.create_user(username='business', password='Pass12345')
        Profile.objects.create(user=self.customer, type='customer')
        Profile.objects.create(user=self.business, type='business')
        self.customer_token = Token.objects.create(user=self.customer)
        self.business_token = Token.objects.create(user=self.business)

        # Angebot + Angebotsdetail
        self.offer = Offer.objects.create(
            user=self.business,
            title='Logo Design',
            description='Logo Design Angebot',
            min_price=100,
            min_delivery_time=5
        )
        self.detail = OfferDetail.objects.create(
            offer=self.offer,
            title='Basic Design',
            revisions=2,
            delivery_time_in_days=5,
            price=150,
            features=['Logo Design', 'Visitenkarte'],
            offer_type='basic'
        )

    def test_create_order_success(self):
        url = '/api/orders/'
        payload = {"offer_detail_id": self.detail.id}
        resp = self.client.post(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.json()
        self.assertEqual(data['customer_user'], self.customer.id)
        self.assertEqual(data['business_user'], self.business.id)
        self.assertEqual(data['title'], self.detail.title)
        self.assertEqual(float(data['price']), 150.0) 
        self.assertEqual(data['offer_type'], self.detail.offer_type)
        self.assertEqual(data['status'], 'in_progress')
        self.assertTrue(Order.objects.filter(customer_user=self.customer, business_user=self.business).exists())

    def test_create_order_forbidden_for_business(self):
        url = '/api/orders/'
        payload = {"offer_detail_id": self.detail.id}
        resp = self.client.post(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {self.business_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_order_unauthenticated(self):
        url = '/api/orders/'
        payload = {"offer_detail_id": self.detail.id}
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_invalid_detail(self):
        url = '/api/orders/'
        payload = {"offer_detail_id": 99999}
        resp = self.client.post(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

class OrderUpdateAPITests(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(username='customer', password='Pass12345')
        self.business = User.objects.create_user(username='business', password='Pass12345')
        Profile.objects.create(user=self.customer, type='customer')
        Profile.objects.create(user=self.business, type='business')
        self.customer_token = Token.objects.create(user=self.customer)
        self.business_token = Token.objects.create(user=self.business)

        self.order = Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title='Logo Design',
            revisions=2,
            delivery_time_in_days=5,
            price=150,
            features=['Logo', 'Card'],
            offer_type='basic',
            status='in_progress'
        )

    def test_patch_order_success(self):
        url = f'/api/orders/{self.order.id}/'
        payload = {"status": "completed"}
        resp = self.client.patch(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {self.business_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(data['status'], 'completed')
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'completed')

    def test_patch_order_forbidden_for_customer(self):
        url = f'/api/orders/{self.order.id}/'
        payload = {"status": "completed"}
        resp = self.client.patch(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_order_invalid_status(self):
        url = f'/api/orders/{self.order.id}/'
        payload = {"status": "invalid_status"}
        resp = self.client.patch(url, payload, format='json', HTTP_AUTHORIZATION=f'Token {self.business_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)




class OrderDeleteAPITests(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(username='customer', password='Pass12345')
        self.business = User.objects.create_user(username='business', password='Pass12345')
        self.admin = User.objects.create_user(username='admin', password='Pass12345', is_staff=True)
        
        Profile.objects.create(user=self.customer, type='customer')
        Profile.objects.create(user=self.business, type='business')
        
        self.customer_token = Token.objects.create(user=self.customer)
        self.business_token = Token.objects.create(user=self.business)
        self.admin_token = Token.objects.create(user=self.admin)

        self.order = Order.objects.create(
            customer_user=self.customer,
            business_user=self.business,
            title='Logo Design',
            revisions=2,
            delivery_time_in_days=5,
            price=150,
            features=['Logo', 'Card'],
            offer_type='basic',
            status='in_progress'
        )

    def test_delete_order_success_admin(self):
        """Only admin can delete"""
        url = f'/api/orders/{self.order.id}/'
        resp = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=self.order.id).exists())

    def test_delete_order_forbidden_for_customer(self):
        """Customer cannot delete"""
        url = f'/api/orders/{self.order.id}/'
        resp = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.customer_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Order.objects.filter(pk=self.order.id).exists())

    def test_delete_order_forbidden_for_business(self):
        """Business user cannot delete"""
        url = f'/api/orders/{self.order.id}/'
        resp = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.business_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Order.objects.filter(pk=self.order.id).exists())

    def test_delete_order_unauthenticated(self):
        """Unauthenticated users get 401"""
        url = f'/api/orders/{self.order.id}/'
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_order_not_found(self):
        """404 if order doesn't exist"""
        url = '/api/orders/99999/'
        resp = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)