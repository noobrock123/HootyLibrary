from django.db import IntegrityError
from django.test import TestCase
from .models import *
from datetime import datetime, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile


class IssueTestCase(TestCase):
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
        self.issue1 = Issue.objects.create(
            issuer=self.user1,
            book_refer=self.book1,
            title='This is issue1 title',
            msg='This is issue1 message'
        )

    def test_create_issue_correct(self):
        # test issue was created correctly
        with self.subTest():
            self.assertEqual(self.issue1.issuer, self.user1)
        with self.subTest():
            self.assertEqual(self.issue1.book_refer, self.book1)
        with self.subTest():
            self.assertEqual(self.issue1.title, 'This is issue1 title')
        with self.subTest():
            self.assertEqual(self.issue1.msg, 'This is issue1 message')

    def test_issue_on_issuer_deleted(self):
        # test issue when issuer was deleted
        self.user1.delete()
        self.issue1.refresh_from_db()
        self.assertEqual(self.issue1.issuer, None)

    def test_issue_on_book_refer_deleted(self):
        # test issue when book_refer was deleted
        self.book1.delete()
        with self.assertRaises(Exception) as raised:
            Issue.objects.get(issuer=self.user1, book_refer=self.book1)
        self.assertEqual(Issue.DoesNotExist, type(raised.exception))

    def test_issue_get_attribs(self):
        # test issue function get_attribs()
        self.assertEqual(self.issue1.get_attribs()[
                         1:], ('This is issue1 title', 'This is issue1 message'))
