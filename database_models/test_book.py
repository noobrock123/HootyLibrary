from django.db import IntegrityError
from django.test import TestCase
from .models import *
from datetime import datetime, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile

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
        self.book3 = Book.objects.create(
            book_name='book3',
            author=self.user2,
            book_type=1,
            genres=('genre1', 'genre2'),
            description='This is book3 description',
            thumbnail=SimpleUploadedFile(name='RH_StudyGuide.jpg', content=open(
            'database_models/data_test/RH_StudyGuide.jpg', 'rb').read(), content_type='image/jpeg')
,
            pdf_files=SimpleUploadedFile(name='RH_StudyGuide_V2.pdf', content=open(
            'database_models/data_test/RH_StudyGuide_V2.pdf', 'rb').read(), content_type='application/pdf'),
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
        with self.subTest():
            self.assertQuerysetEqual(self.book2.genres.all(), [
                                     self.genre1, self.genre2], ordered=False)
        with self.subTest():
            self.assertTrue(
                self.book2.book_name == 'book2' and
                self.book2.author == self.user2 and
                self.book2.book_type == 2 and
                True
            )

    def test_book_create_correct_by_others(self):

        pdf_files = SimpleUploadedFile(name='RH_StudyGuide_V2.pdf', content=open(
            'database_models/data_test/RH_StudyGuide_V2.pdf', 'rb').read(), content_type='application/pdf')
        thumbnail = SimpleUploadedFile(name='RH_StudyGuide.jpg', content=open(
            'database_models/data_test/RH_StudyGuide.jpg', 'rb').read(), content_type='image/jpeg')

        book4 = Book.objects.create(
            book_name='book4',
            author=self.user2,
            book_type=1,
            genres=('genre1', 'genre2'),
            description='This is book4 description',
            thumbnail=thumbnail,
            pdf_files=pdf_files,
        )
        with self.subTest():
            with open(book4.thumbnail.path, 'rb') as thumbnail1, open('database_models/data_test/RH_StudyGuide.jpg', 'rb').read() as thumbnail2:
                self.assertEqual(thumbnail1.read(), thumbnail2.read())
        with self.subTest():
            with open(book4.pdf_files.path, 'rb') as pdf_files1, open('database_models/data_test/RH_StudyGuide.jpg', 'rb').read() as pdf_files2:
                self.assertEqual(pdf_files1.read(), pdf_files2.read())

        with self.subTest():
            self.assertQuerysetEqual(self.book1.genres.all(), [
                                     self.genre1], ordered=False)
        with self.subTest():
            self.assertTrue(
                self.book1.book_name == 'book1' and
                self.book1.description == '' and
                self.book1.author == self.user1 and
                self.book1.book_type == 1 and
                True
            )

    def test_book_create_when_genres_not_exit(self):

        with self.assertRaises(Exception) as raised:
            book3 = Book.objects.create(
                book_name='book3',
                author=self.user1,
                book_type=3,
                genres=('genre3', )
            )
        self.assertEqual(ValueError, type(raised.exception))
    