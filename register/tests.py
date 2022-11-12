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
            email='email1@email.email',
        )
    def test_view_register(self):
        c = Client(enforce_csrf_checks=True)
        response = c.get('/registeration/sign_up/')
        with self.subTest():

            self.assertEqual(response.status_code, 200)
        with self.subTest():
            self.assertTemplateUsed(response, 'register/templates/sign_up_and_in/signup.html')
    def test_view_register_registration_success(self):
        c = Client()
        form = {
            'username':'user2',
            'email':'user2@email.email',
            'password':'password',
            'confirm_password':'password'
            }
        response = c.post('/registeration/sign_up/', form,format='text/html')
        messages = list(get_messages(response.wsgi_request))
        # print(messages)
        user2 = User.objects.get(username='user2')
        with self.subTest():
            self.assertEqual(response.status_code, 302)
        with self.subTest():
            self.assertTemplateUsed(response, 'MAIN_APP/templates/homepage/homepage.html')

        with self.subTest():
            self.assertEqual(str(messages[0]), f'{user2.username}:{user2.alias_name} successful to log in',)

    def test_view_register_registration_failed_username_used(self):
        c = Client()
        form = {
            'username':'user1',
            'email':'user2@email.email',
            'password':'password',
            'confirm_password':'password'
            }
        response = c.post('/registeration/sign_up/', form,format='text/html')
        messages = list(get_messages(response.wsgi_request))
        # print(messages)
        with self.subTest():
            self.assertEqual(response.status_code, 200)
        with self.subTest():
            self.assertTemplateUsed(response, 'register/templates/sign_up_and_in/signup.html')
        with self.subTest():
            self.assertEqual(str(messages[0]), 'This username is already exists')
    # def test_view_register_registration_failed_username_used(self):
    #     c = Client()
    #     form = {
    #         'username':'user1',
    #         'email':'user2@email.email',
    #         'password':'password',
    #         'confirm_password':'password'
    #         }
    #     response = c.post('/registeration/sign_up/', form,format='text/html')
    #     messages = list(get_messages(response.wsgi_request))
    #     # print(messages)
    #     with self.subTest():
    #         self.assertEqual(response.status_code, 200)
    #     with self.subTest():
    #         self.assertTemplateUsed(response, 'register/templates/sign_up_and_in/signup.html')
    #     with self.subTest():
    #         self.assertEqual(str(messages[0]), 'This username is already exists')
    