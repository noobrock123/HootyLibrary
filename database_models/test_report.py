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
        self.report1 = Report.objects.create(
            reporter=self.user1,
            book_refer=self.book1,
            title='This is report1 title',
            msg='This is report1 message'
        )

    def test_create_report_correct(self):
        # test report was created correctly
        with self.subTest():
            self.assertEqual(self.report1.reporter, self.user1)
        with self.subTest():
            self.assertEqual(self.report1.book_refer, self.book1)
        with self.subTest():
            self.assertEqual(self.report1.title, 'This is report1 title')
        with self.subTest():
            self.assertEqual(self.report1.msg, 'This is report1 message')

    def test_report_on_reporter_deleted(self):
        # test report when reporter was deleted
        self.user1.delete()
        self.report1.refresh_from_db()
        self.assertEqual(self.report1.reporter, None)

    def test_report_on_book_refer_deleted(self):
        # test report when book_refer was deleted
        self.book1.delete()
        with self.assertRaises(Exception) as raised:
            Report.objects.get(reporter=self.user1, book_refer=self.book1)
        self.assertEqual(Report.DoesNotExist, type(raised.exception))

    def test_report_get_attribs(self):
        # test report function get_attribs()
        self.assertEqual(self.report1.get_attribs()[
                         1:], ('This is report1 title', 'This is report1 message'))
