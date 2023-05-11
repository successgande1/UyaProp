from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from account.forms import RegistrationForm
from realestate.models import Landlord, Agent, Prospect

class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register-account')

    def test_register_view_success(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'user_type': 'landlord'
        }
        form = RegistrationForm(data)
        self.assertTrue(form.is_valid())
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('success-account'))

        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('testpassword'))

        landlord = Landlord.objects.get(user=user)
        self.assertIsNotNone(landlord)

    def test_register_view_invalid_form(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'wrongpassword',
            'user_type': 'landlord'
        }
        form = RegistrationForm(data)
        self.assertFalse(form.is_valid())
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')

        form = response.context['form']
        self.assertTrue(form.has_error('password2'))

        user_exists = User.objects.filter(username='testuser').exists()
        self.assertFalse(user_exists)
