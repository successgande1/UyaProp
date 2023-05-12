from django.urls import reverse
from django.test import Client, TestCase
from django.contrib.auth.models import User
from realestate.models import Landlord
from account.forms import RegistrationForm


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register-account')
        self.success_url = reverse('success-account')

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
        self.assertRedirects(response, self.success_url)

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