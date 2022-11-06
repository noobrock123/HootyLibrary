from django.db import IntegrityError
from django.test import TestCase
from .models import *
# Create your tests here.


class CreateUserTestCase(TestCase):
    def setUp(self) -> None:
        user1 = User.objects.create_user(
            user_id='0x79521458',
            username='user1',
            password='password',
            email='user1@email.email'
        )

    def test_create_user_correct(self):
        user2 = User.objects.create_user(
            user_id='0x79521457',
            username='user2',
            password='password',
            email='user2@email.email'
        )
        self.assertTrue(
            user2.user_id == '0x79521457' and
            user2.username == 'user2' and
            user2.check_password('password') and
            user2.email == 'user2@email.email'

        )

    def test_user_id_is_unique(self):
        with self.assertRaises(Exception) as raised:
            user2 = User.objects.create_user(
                user_id='0x79521458',
                username='user2',
                password='password',
                email='user2@email.email'
            )
        self.assertEqual(ValidationError, type(raised.exception))

    def test_user_id_generate_when_null(self):

        user2 = User.objects.create_user(
            user_id=None,
            username='user2',
            password='password',
            email='user2@email.email'
        )
        self.assertNotEqual(None, user2.user_id)

    def test_user_id_generate_when_blank(self):

        user2 = User.objects.create_user(
            user_id='',
            username='user2',
            password='password',
            email='user2@email.email'
        )
        self.assertNotEqual('', user2.user_id)

    def test_username_is_unique(self):
        with self.assertRaises(Exception) as raised:
            user2 = User.objects.create_user(
                username='user1',
                password='password',
                email='user2@email.email'
            )
        self.assertEqual(ValidationError, type(raised.exception))

    def test_username_not_null(self):
        with self.assertRaises(Exception) as raised:
            user1 = User.objects.create_user(
                username=None,
                password='password',
                email='user1@email.email',
            )
        self.assertEqual(ValidationError, type(raised.exception))

    def test_username_not_blank(self):
        with self.assertRaises(Exception) as raised:
            user1 = User.objects.create_user(
                username='',
                password='password',
                email='user1@email.email',
            )
        self.assertEqual(ValidationError, type(raised.exception))

    def test_username_not_exceed_max_length(self):
        with self.assertRaises(Exception) as raised:
            User.objects.create_user(
                username='user123456789101112131415161718192021222324',
                password='password',
                email='user1@email.email',
            )
        self.assertEqual(ValidationError, type(raised.exception))

    def test_email_is_unique(self):
        with self.assertRaises(Exception) as raised:
            User.objects.create_user(
                user_id='0x79521457',
                username='user2',
                password='password',
                email='user1@email.email'
            )
        self.assertEqual(ValidationError, type(raised.exception))

    def test_email_is_in_email_form(self):
        with self.assertRaises(Exception) as raised:
            User.objects.create_user(
                user_id='0x79521457',
                username='user2',
                password='password',
                email='user@email'
            )
        self.assertEqual(ValidationError, type(raised.exception))
