from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')

    def test_not_authenticated(self):
        """Ensure blocking of any non authenticated users"""
        response = self.client.get(reverse('vehicles:index'))
        self.assertRedirects(response, '/login?next=/vehicles')

        response = self.client.get(reverse('vehicles:trip_begin'))
        self.assertRedirects(response, '/login?next=/vehiclestrip_begin')

        response = self.client.get(reverse('vehicles:trip_finish'))
        self.assertRedirects(response, '/login?next=/vehiclestrip_finish')

    def test_authenticated(self):
        login_successful = self.client.login(username=self.user.username, password='pass')
        self.assertTrue(login_successful)

        # Make sure index takes user to home page
        response = self.client.get(reverse('vehicles:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "vehicles/home.html")


class TripBeginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        login_successful = self.client.login(username=self.user.username, password='pass')
        self.assertTrue(login_successful)

    def test_not_post(self):
        """Only PUT request is allowed"""
        response = self.client.get(reverse('vehicles:trip_begin'))
        self.assertEqual(response.status_code, 405)

        response = self.client.head(reverse('vehicles:trip_begin'))
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(reverse('vehicles:trip_begin'))
        self.assertEqual(response.status_code, 405)

        response = self.client.options(reverse('vehicles:trip_begin'))
        self.assertEqual(response.status_code, 405)
