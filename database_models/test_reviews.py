from django.db import IntegrityError
from django.test import TestCase
from .models import *
from datetime import datetime, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from django.dispatch import receiver


class ReviewTestCase(TestCase):
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
                'database_models/data_test/RH_StudyGuide.jpg', 'rb').read(), content_type='image/jpeg'),
            pdf_files=SimpleUploadedFile(name='RH_StudyGuide_V2.pdf', content=open(
                'database_models/data_test/RH_StudyGuide_V2.pdf', 'rb').read(), content_type='application/pdf'),
        )
        self.review1 = Review.objects.create(
            reviewer=self.user1,
            book_refer=self.book1,
            score=12,
            title='This is title review1',
            msg='This is message review1',
        )

    def test_create_review_correct(self):
        # test review was created correctly
        with self.subTest():
            self.assertEqual(self.review1.reviewer, self.user1)
        with self.subTest():
            self.assertEqual(self.review1.book_refer, self.book1)
        with self.subTest():
            self.assertEqual(self.review1.score, 12)
        with self.subTest():
            self.assertEqual(self.review1.title, 'This is title review1')
        with self.subTest():
            self.assertEqual(self.review1.msg, 'This is message review1')

    def test_pair_of_reviewer_book_is_unique(self):
        # test pair of reviewer, book_refer is uniquely
        with self.subTest():
            with self.assertRaises(Exception) as raised:

                self.review2 = Review.objects.create(
                    reviewer=self.user1,
                    book_refer=self.book1,
                    score=11,
                    title='This is title review2',
                    msg='This is message review2'
                )
            self.assertEqual(ValidationError, type(raised.exception))

    def test_review_reviewer_on_delete(self):
        # test review when reviewer was deleted
        self.user1.delete()
        with self.assertRaises(Exception) as raised:
            Review.objects.get(reviewer=self.user1, book_refer=self.book1)
        self.assertEqual(Review.DoesNotExist, type(raised.exception))

    def test_review_book_refer_on_delete(self):
        # test review when book_refer was deleted
        self.book1.delete()
        with self.assertRaises(Exception) as raised:
            Review.objects.get(reviewer=self.user1, book_refer=self.book1)
        self.assertEqual(Review.DoesNotExist, type(raised.exception))
