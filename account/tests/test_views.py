from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from realestate.models import Landlord, Agent, Prospect
from account.forms import RegistrationForm

class RegistrationViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_registration_view_post(self):
        # create a POST request with valid form data
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'user_type': 'landlord',
        })

        # check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # check that the user was created
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)

        # check that the correct user type object was created
        landlord = Landlord.objects.filter(user=user).first()
        self.assertIsNotNone(landlord)
        self.assertIsNone(Agent.objects.filter(user=user).first())
        self.assertIsNone(Prospect.objects.filter(user=user).first())

    def test_registration_view_get(self):
        # create a GET request
        response = self.client.get(self.register_url)

        # check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # check that the correct template is used
        self.assertTemplateUsed(response, 'account/register.html')

        # check that the RegistrationForm is in the context
        self.assertIsInstance(response.context['form'], RegistrationForm)
