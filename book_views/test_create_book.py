from django.test import Client, TestCase
from database_models.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, timedelta
# Create your tests here.


class CreateBookTestCase(TestCase):
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
        self.user3 = User.objects.create_user(
            username='user3',
            password='password',
            email='user3@email.email'
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
                'book_views/test_data/RH_StudyGuide_V2.pdf', 'rb').read(), content_type='image/jpeg'),
            pdf_files=SimpleUploadedFile(name='RH_StudyGuide_V2.pdf', content=open(
                'book_views/test_data/RH_StudyGuide_V2.pdf', 'rb').read(), content_type='application/pdf'),
        )
        self.review1 = Review.objects.create(
            reviewer=self.user1,
            book_refer=self.book1,
            title='review1 title',
            score=5,
            msg='review1 msg'
        )
        self.review2 = Review.objects.create(
            reviewer=self.user2,
            book_refer=self.book1,
            score=8,
            title='review2 title',
            msg='review2 msg'
        )
        self.issue1 = Issue.objects.create(
            issuer=self.user1,
            book_refer=self.book1,
            title='issue1 title',
            msg='issue1 msg'
        )
        self.favorite1 = Favorite.objects.create(
            user_refer=self.user1,
            book_refer=self.book1,
        )
        self.read1 = Read.objects.create(
            user_refer=self.user1,
            book_refer=self.book1,
        )

    
    
    
    def test_client_redirect_create_book_on_user_not_login(self):
        # test client can redirect create book on user not login
        c = Client()
        response = c.get(f'/book/create_book/')

        with self.subTest():
            self.assertRedirects(response, '/registeration/sign_in/?next=/book/create_book/', status_code=302,
                                 target_status_code=200, fetch_redirect_response=True)

    def test_client_can_access_create_book_on_user_logged_in(self):
        # test client can access create book on user logged in
        c = Client()
        c.login(username='user1', password='password')
        response = c.get(f'/book/create_book/')
        with self.subTest():
            self.assertEqual(response.status_code, 200)
        with self.subTest():
            self.assertQuerysetEqual(response.context['genres'], [
                                     self.genre1, self.genre2], ordered=False)
        with self.subTest():
            self.assertTemplateUsed(
                response, 'book_views/templates/book_views/create_book.html')

    def test_client_create_book_success(self):
        # test client can create book success and correctly
        c = Client()
        c.login(username='user1', password='password')

        post = {
            'book_name': 'created_book',
            'description': 'created_book_description',
            'book_type': 1,
            'genres': ['genre1', 'genre2'],
            'thumbnail': SimpleUploadedFile(name='RH_StudyGuide_V2.pdf', content=open(
                'book_views/test_data/RH_StudyGuide.jpg', 'rb').read(), content_type='image/jpeg'),
            'pdf_files': SimpleUploadedFile(name='RH_StudyGuide_V2.pdf', content=open(
                'book_views/test_data/RH_StudyGuide_V2.pdf', 'rb').read(), content_type='application/pdf'),
        }
        response = c.post(f'/book/create_book/', data=post)
        with self.subTest():
            self.assertEqual(response.status_code, 302)
        book = Book.objects.filter(author=self.user1).latest('date_created')
        with self.subTest():
            self.assertEqual(book.book_name, 'created_book')
        with self.subTest():
            self.assertEqual(book.description, 'created_book_description')
        with self.subTest():
            time_now = timezone.now()
            self.assertTrue(
                book.date_created <= time_now and book.date_created + timedelta(seconds=1) > time_now)
        with self.subTest():
            self.assertEqual(book.book_type, 1)
        with self.subTest():
            self.assertQuerysetEqual(
                book.genres.all(), [self.genre1, self.genre2], ordered=False)
        with self.subTest():
            self.assertEqual(book.author, self.user1)
        with self.subTest():
            with open('book_views/test_data/RH_StudyGuide.jpg', 'rb') as thumbnail, open(f'{book.thumbnail.path}', 'rb') as created_book_thumbnail:
                self.assertEqual(
                    created_book_thumbnail.read(), thumbnail.read())
        with self.subTest():
            with open('book_views/test_data/RH_StudyGuide_V2.pdf', 'rb') as pdf, open(f'{book.pdf_files.path}', 'rb') as created_book_pdf:
                self.assertEqual(created_book_pdf.read(), pdf.read())

    def test_client_create_book_unsuccess_no_book_name(self):
        # test client create book unsuccess when no book name
        c = Client()
        c.login(username='user1', password='password')

        post = {
            'description': 'created_book_description',
            'book_type': 1,
            'genres': ['genre1', 'genre2'],
            'thumbnail': SimpleUploadedFile(name='RH_StudyGuide_V2.pdf', content=open(
                'book_views/test_data/RH_StudyGuide.jpg', 'rb').read(), content_type='image/jpeg'),
            'pdf_files': SimpleUploadedFile(name='RH_StudyGuide_V2.pdf', content=open(
                'book_views/test_data/RH_StudyGuide_V2.pdf', 'rb').read(), content_type='application/pdf'),
        }
        response = c.post(f'/book/create_book/', data=post)
        self.assertEqual(Book.objects.filter(author=self.user1).count(), 1)

    def test_client_create_book_unsuccess_no_book_type(self):
        # test client create book unsuccess when no book type
        c = Client()
        c.login(username='user1', password='password')

        post = {
            'description': 'created_book_description',
            'book_type': 1,
            'genres': ['genre1', 'genre2'],
            'thumbnail': SimpleUploadedFile(name='RH_StudyGuide_V2.pdf', content=open(
                'book_views/test_data/RH_StudyGuide.jpg', 'rb').read(), content_type='image/jpeg'),
            'pdf_files': SimpleUploadedFile(name='RH_StudyGuide_V2.pdf', content=open(
                'book_views/test_data/RH_StudyGuide_V2.pdf', 'rb').read(), content_type='application/pdf'),
        }
        response = c.post(f'/book/create_book/', data=post)
        self.assertEqual(Book.objects.filter(author=self.user1).count(), 1)
    
    
    