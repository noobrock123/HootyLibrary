from django.test import TestCase
from database_models.models import *
from django.test import Client
from django.contrib import auth
from django.contrib.auth import SESSION_KEY
from django.contrib.messages import get_messages
# Create your tests here.


class RegisterTestCase(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username='user1',
            password='password',
            email='user1@email.email',
        )

    def test_view_register(self):
        # test client can access register
        c = Client(enforce_csrf_checks=True)
        response = c.get('/registeration/sign_up/')
        with self.subTest():

            self.assertEqual(response.status_code, 200)
        with self.subTest():
            self.assertTemplateUsed(
                response, 'register/templates/sign_up_and_in/signup.html')

    def test_view_register_registration_success(self):
        # test client registration successful & redirect
        c = Client()
        form = {
            'username': 'user2',
            'email': 'user2@email.email',
            'password': 'password',
            'confirm_password': 'password'
        }
        response = c.post('/registeration/sign_up/', form, format='text/html')
        messages = list(get_messages(response.wsgi_request))
        user2 = User.objects.get(username='user2')
        with self.subTest():
            self.assertRedirects(response, '/', status_code=302,
                                 target_status_code=200, fetch_redirect_response=True)

        with self.subTest():
            self.assertEqual(
                str(messages[0]), f'{user2.username}:{user2.alias_name} create user successful',)

    def test_view_register_registration_failed_username_used(self):
        # test client when enter used username
        c = Client()
        form = {
            'username': 'user1',
            'email': 'user2@email.email',
            'password': 'password',
            'confirm_password': 'password'
        }
        response = c.post('/registeration/sign_up/', form, format='text/html')
        messages = list(get_messages(response.wsgi_request))
        with self.subTest():
            self.assertEqual(response.status_code, 200)
        with self.subTest():
            self.assertTemplateUsed(
                response, 'register/templates/sign_up_and_in/signup.html')
        with self.subTest():
            self.assertEqual(str(messages[0]),
                             'This username is already exists')

    def test_view_register_registration_failed_email_used(self):
        # test client when enter used email
        c = Client()
        form = {
            'username': 'user2',
            'email': 'user1@email.email',
            'password': 'password',
            'confirm_password': 'password'
        }
        response = c.post('/registeration/sign_up/', form, format='text/html')
        messages = list(get_messages(response.wsgi_request))
        with self.subTest():
            self.assertEqual(response.status_code, 200)
        with self.subTest():
            self.assertTemplateUsed(
                response, 'register/templates/sign_up_and_in/signup.html')
        with self.subTest():
            self.assertEqual(str(messages[0]), 'This email is already exists')

    def test_view_register_registration_failed_password_not_match(self):
        # test client when enter password not match
        c = Client()
        form = {
            'username': 'user2',
            'email': 'user2@email.email',
            'password': 'password',
            'confirm_password': 'password1'
        }
        response = c.post('/registeration/sign_up/', form, format='text/html')
        messages = list(get_messages(response.wsgi_request))
        with self.subTest():
            self.assertEqual(response.status_code, 200)
        with self.subTest():
            self.assertTemplateUsed(
                response, 'register/templates/sign_up_and_in/signup.html')
        with self.subTest():
            self.assertEqual(str(messages[0]), 'Password do not match')
