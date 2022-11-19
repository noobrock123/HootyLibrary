from django.test import TestCase
from database_models.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.contrib.messages import get_messages


class UserProfileTestCase(TestCase):
    def setUp(self) -> None:
        with open('userProfile/test_media/owl.jpg', 'rb') as profile_pic:
            self.user1 = User.objects.create_user(
                username='user1',
                alias_name='user1_alias_name',
                email='user1@email.email',
                password='password',
                gender="Garfiw'sGender",
                age=16,
                occupation='user1 occupation',
                bio='user bio',
                social_link='www.user1_social_link.user1',
                donation_link='www.user1_donation_link.user1',
                profile_pic=SimpleUploadedFile(
                    name='owl.jpg', content=profile_pic.read(), content_type='image/jpeg'),
            )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@email.email',
            password='password'
        )
        self.genre1 = Genre.objects.create(
            genre_list='genre1'
        )
        self.genre2 = Genre.objects.create(
            genre_list='genre2'
        )
        self.book1 = Book.objects.create(
            book_name='book1',
            author=self.user1,
            book_type=1,
            genres=('genre1', )
        )
        self.book2 = Book.objects.create(
            book_name='book2',
            author=self.user2,
            book_type=2,
            genres=('genre1', 'genre2')
        )

    def test_client_can_access_user_profile_picture(self):
        # test client can access user profile picture
        c = Client()
        response = c.get(f'/user_profile/user_picture/{self.user1.user_id}/')
        self.assertEqual(response.status_code, 200)

    def test_client_can_access_user_profile(self):
        # test client can access user profile
        c = Client()
        response = c.get(f'/user_profile/{self.user1.user_id}/')
        self.assertEqual(response.status_code, 200)

    def test_client_access_user_profile_picture_correct(self):
        # test client get user profile picture correct
        c = Client()
        response = c.get(f'/user_profile/user_picture/{self.user1.user_id}/')
        with open(self.user1.profile_pic.path, 'rb') as profile_pic:
            self.assertEqual(response.content, profile_pic.read())

    def test_client_access_user_profile_not_set(self):
        # test client get user profile picture when owener user do not set picture profile
        c = Client()
        response = c.get(f'/user_profile/user_picture/{self.user2.user_id}/')
        with open('userProfile/static/userProfile/images/default_user_profile.png', 'rb') as default_profile_pic:
            self.assertEqual(response.content, default_profile_pic.read())

    def test_client_access_user_profile_correct(self):
        # test client get user profile correct
        c = Client()
        response = c.get(f'/user_profile/{self.user1.user_id}/')
        with self.subTest():
            self.assertQuerysetEqual(response.context['my_books'], [
                                     self.book1, ], ordered=False)
        with self.subTest():
            self.assertEqual(response.context['bio'], 'user bio')
        with self.subTest():
            self.assertEqual(response.context['username'], 'user1')
        with self.subTest():
            self.assertEqual(response.context['gender'], "Garfiw'sGender")
        with self.subTest():
            self.assertEqual(
                response.context['occupation'], 'user1 occupation')
        with self.subTest():
            self.assertEqual(
                response.context['link'], ('www.user1_social_link.user1', 'www.user1_donation_link.user1'))
        with self.subTest():
            self.assertEqual(response.context['user_id'], self.user1.user_id)
