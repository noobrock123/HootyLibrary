from django.db import IntegrityError
from django.test import TestCase
from .models import *
from datetime import datetime, timedelta
# Create your tests here.


class BookTestCase(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username='user1',
            password='password',
            email='user1@email.email'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password',
            email='user2@email.email'
        )
        self.genre1 = Genre.objects.create(
            genre_list='genre1'
        )
        self.book1 = Book.objects.create(
            book_name='book1',
            author=self.user1,
            book_type=1,
            genres=('genre1', )
        )
        self.book1 = Book.objects.create(
            book_name='book1',
            author=self.user1,
            book_type=1,
            genres=('genre1', )
        )

    def test_book_create_correct_by_default(self):
        with self.subTest():
            self.assertQuerysetEqual(self.book1.genres.all(), [
                                     self.genre1], ordered=False)
        with self.subTest():
            self.assertTrue(
                self.book1.book_name == 'book1' and
                self.book1.author == self.user1 and
                self.book1.book_type == 1 and
                True
            )
    # def test_book_create_correct_by_others(self):
    #     book2 = Book.objects.create(
    #         book_name='',

    #     )
    #     with self.subTest():
    #         self.assertQuerysetEqual(self.book1.genres.all(), [
    #                                  self.genre1], ordered=False)
    #     with self.subTest():
    #         self.assertTrue(
    #             self.book1.book_name == 'book1' and
    #             self.book1.description == ''
    #             self.book1.author == self.user1 and
    #             self.book1.book_type == 1 and
    #             True
    #         )

    def test_book_create_with_genres_not_exit(self):

        with self.assertRaises(Exception) as raised:
            book2 = Book.objects.create(
                book_name='book2',
                author=self.user1,
                book_type=1,
                genres=('genre2', )
            )
        self.assertEqual(ValueError, type(raised.exception))
