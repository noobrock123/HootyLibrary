from django.db import IntegrityError
from django.test import TestCase
from .models import *
from datetime import datetime, timedelta
# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self) -> None:
        user1 = User.objects.create_user(
            username='user1',
            password='password',
            email='user1@email.email'
        )

    def test_create_normal_user_correct(self):
        user2 = User.objects.create_user(
            username='user2',
            password='password',
            email='user2@email.email'
        )
        # print(user2.date_joined)
        # print(timezone.now())
        self.assertTrue(
            user2.username == 'user2' and
            user2.check_password('password') and
            user2.email == 'user2@email.email' and
            timezone.now() < user2.date_joined + timedelta(seconds=1) and
            user2.gender == None and
            user2.age == None and
            user2.occupation == None and
            user2.bio == '' and
            user2.social_link == None and
            user2.donation_link == None and
            user2.profile_pic == None and
            user2.is_staff == 0 and
            user2.is_active == 1 and
            True

        )

    def test_create_superuser_correct(self):
        admin = User.objects.create_superuser(

            username='admin',
            password='password',
            email='admin@email.email'
        )

        self.assertTrue(

            admin.username == 'admin' and
            admin.check_password('password') and
            admin.email == 'admin@email.email' and
            timezone.now() < admin.date_joined + timedelta(seconds=1) and
            admin.gender == None and
            admin.age == None and
            admin.occupation == None and
            admin.bio == '' and
            admin.social_link == None and
            admin.donation_link == None and
            admin.profile_pic == None and
            admin.is_staff == 1 and
            admin.is_active == 1 and
            admin.is_superuser == 1 and
            True

        )

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

                username='user2',
                password='password',
                email='user1@email.email'
            )
        self.assertEqual(ValidationError, type(raised.exception))

    def test_email_is_in_email_form(self):
        with self.assertRaises(Exception) as raised:
            User.objects.create_user(

                username='user2',
                password='password',
                email='user@email'
            )
        self.assertEqual(ValidationError, type(raised.exception))

    def test_date_joined_is_uneditable(self):
        user1 = User.objects.create_user(
            username='user2',
            password='password',
            email='user2@email.email'
        )
        prev = user1.date_joined
        user1.date_joined = timezone.now() + timedelta(days=20)
        user1.save()
        post = user1.date_joined
        self.assertEqual(prev, post)
