from django.db import IntegrityError
from django.test import TestCase
from .models import *
from datetime import datetime, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username='user1',
            password='password',
            email='user1@email.email',
            alias_name='user1 alias_name',
            gender='user1 gender',
            age=10,
            occupation='user1 occupation',
            bio='user1 bio',
            social_link='user1 social_link',
            donation_link='user1 donation_link',
            profile_pic=SimpleUploadedFile(name='owl.jpg', content=open(
                'database_models/data_test/owl.jpg', 'rb').read(), content_type='image/jpeg'),

        )
    def test_user_str(self):
        # test user __str__
        self.assertEqual(f'{self.user1.user_id}: {self.user1.username}', str(self.user1))
    def test_create(self):
        # test create
        user2 = User.objects.create(
            username='user2',
            password='password',
            email='user2@email.email'
        )
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
    def test_create_normal_user_correct(self):
        # test normal user was create correctly
        user2 = User.objects.create_user(
            username='user2',
            password='password',
            email='user2@email.email'
        )
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
        # test super user was create correctly
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
        # test username is uniquely
        with self.assertRaises(Exception) as raised:
            user2 = User.objects.create_user(
                username='user1',
                password='password',
                email='user2@email.email'
            )
        self.assertEqual(ValidationError, type(raised.exception))

    def test_username_not_null(self):
        # test username can not be null
        with self.assertRaises(Exception) as raised:
            user1 = User.objects.create_user(
                username=None,
                password='password',
                email='user1@email.email',
            )
        self.assertEqual(ValidationError, type(raised.exception))

    def test_username_not_blank(self):
        # test username can not be blank
        with self.assertRaises(Exception) as raised:
            user1 = User.objects.create_user(
                username='',
                password='password',
                email='user1@email.email',
            )
        self.assertEqual(ValidationError, type(raised.exception))

    def test_username_not_exceed_max_length(self):
        # test username length can not exceed max_length
        with self.assertRaises(Exception) as raised:
            User.objects.create_user(
                username='user123456789101112131415161718192021222324',
                password='password',
                email='user1@email.email',
            )
        self.assertEqual(ValidationError, type(raised.exception))

    def test_email_is_unique(self):
        # test email is uniquely
        with self.assertRaises(Exception) as raised:
            User.objects.create_user(

                username='user2',
                password='password',
                email='user1@email.email'
            )
        self.assertEqual(ValidationError, type(raised.exception))

    def test_email_is_in_email_form(self):
        # test email is in email form
        with self.assertRaises(Exception) as raised:
            User.objects.create_user(

                username='user2',
                password='password',
                email='user@email'
            )
        self.assertEqual(ValidationError, type(raised.exception))

    def test_date_joined_is_uneditable(self):
        # test date joined can not edit
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

    def test_user_email_not_empty(self):
        # test user email can not be empty
        with self.assertRaises(Exception) as raised:
            user1 = User.objects.create(
                username='user2',
                passowrd='password',
                email=''
            )
        self.assertEqual(TypeError, type(raised.exception))

    def test_user_email_not_None(self):
        # test user email can not be null
        with self.assertRaises(Exception) as raised:
            user1 = User.objects.create(
                username='user2',
                passowrd='password',
                email=None
            )
        self.assertEqual(TypeError, type(raised.exception))

    def test_user_get_about_self(self):
        # test user function get_about_self
        self.assertEqual(self.user1.get_about_self(),
                         ('user1 gender', 10, 'user1 occupation',))
    def test_user_get_links(self):
        # test user function get_link
        self.assertEqual(self.user1.get_links(),
        ('user1 social_link', 'user1 donation_link')
        )
