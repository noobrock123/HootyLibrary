from django.db import IntegrityError
from django.test import TestCase
from .models import *
from datetime import datetime, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
class ReadTestCase(TestCase):
    def setUp(self):
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
            author=self.user2,
            book_type=1,
            genres=('genre1', 'genre2'),
            description='This is book1 description',
            thumbnail=SimpleUploadedFile(name='RH_StudyGuide.jpg', content=open(
            'database_models/data_test/RH_StudyGuide.jpg', 'rb').read(), content_type='image/jpeg')
,
            pdf_files=SimpleUploadedFile(name='RH_StudyGuide_V2.pdf', content=open(
            'database_models/data_test/RH_StudyGuide_V2.pdf', 'rb').read(), content_type='application/pdf'),
        )
        self.read1 = Read.objects.create(
            user_refer=self.user1,
            book_refer=self.book1,
        )
    def test_create_read_correct(self):
        with self.subTest():
            self.assertEqual(self.read1.user_refer,self.user1)
        with self.subTest():
            self.assertEqual(self.read1.book_refer, self.book1)
    def test_pair_of_user_book_is_unique(self):
        with self.subTest():
            with self.assertRaises(Exception) as raised:
        
                self.read2 = Read.objects.create(
                    user_refer=self.user1,
                    book_refer=self.book1,
                )
            self.assertEqual(IntegrityError, type(raised.exception))