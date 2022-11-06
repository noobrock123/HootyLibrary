from django.db import IntegrityError
from django.test import TestCase
from .models import *
# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self) -> None:
        self.admin = User.objects.create_superuser(
            username='admin',
            password='password',
            email='admin@email.email'
        )

    def test_user_id_is_unique(self):
        user1 = User.objects.create_user(
            user_id='0x79521458',
            username='user1',
            password='password',
            email='user1@email.email'
        )
        with self.assertRaises(Exception) as raised:
            user2 = User.objects.create_user(
                user_id='0x79521458',
                username='user2',
                password='password',
                email='user2@email.email'
            )
        self.assertEqual(ValidationError, type(raised.exception))

    def test_user_id_generate_when_null(self):
        user1 = User.objects.create_user(
            user_id=None,
            username='user1',
            password='password',
            email='user1@email.email'
        )
        self.assertNotEqual(None, user1.user_id)

    def test_user_id_generate_when_blank(self):
        user1 = User.objects.create_user(
            user_id='',
            username='user1',
            password='password',
            email='user1@email.email'
        )
        self.assertNotEqual('', user1.user_id)

    def test_user_id_is_different(self):
        user1 = User.objects.create_user(
            user_id='0x79521458',
            username='user1',
            password='password',
            email='user1@email.email'
        )
        raised = False
        try:
            user2 = User.objects.create_user(
                user_id='0x79521451',
                username='user2',
                password='password',
                email='user2@email.email'
            )
        except:
            raised = True
        self.assertFalse(raised)

    def test_username_is_unique(self):
        user1 = User.objects.create_user(
            username='user1',
            password='password',
            email='user1@email.email'
        )
        try:
            user2 = User.objects.create_user(
                username='user1',
                password='password',
                email='user2@email.email'
            )
        except Exception as e:
            pass

    def test_username_is_different(self):
        user1 = User.objects.create_user(
            username='user1',
            password='password',
            email='user1@email.email'
        )
        raised = False
        try:
            user2 = User.objects.create_user(
                username='user2',
                password='password',
                email='user2@email.email'
            )
        except:
            raised = True
        self.assertFalse(raised)

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
            user1 = User.objects.create_user(
                username='user123456789101112131415161718192021222324',
                password='password',
                email='user1@email.email',
            )
        self.assertEqual(ValidationError, type(raised.exception))
