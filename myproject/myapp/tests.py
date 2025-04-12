from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class UserAuthenticationTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', email='user@example.com', password='password123')
        self.client = Client()

    def test_register_user_success(self):
        # Test successful registration
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'password123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_user_password_mismatch(self):
        # Test registration with mismatched passwords
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'password456',
        })
        self.assertEqual(response.status_code, 302)  # Redirect back to register page
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_register_user_existing_username(self):
        # Test registration with an existing username
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'password123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect back to register page
        self.assertEqual(User.objects.filter(username='testuser').count(), 1)

    def test_login_user_success(self):
        # Test successful login
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home page
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_user_invalid_credentials(self):
        # Test login with invalid credentials
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 302)  # Redirect back to login page
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_user(self):
        # Test logout functionality
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_home_page_access_authenticated(self):
        # Test access to home page for authenticated users
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)  # Home page is accessible

    def test_home_page_access_unauthenticated(self):
        # Test access to home page for unauthenticated users
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page
