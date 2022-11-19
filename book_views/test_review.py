from django.test import Client, TestCase
from database_models.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, timedelta
# Create your tests here.


class Create_Book(TestCase):
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
        
    def test_client_access_review_on_not_logged_in(self):
        # test client access review on not logged in
        # should redirect to book page
        c = Client()
        response = c.get(f'/book/{self.book1.book_id}/review/')
        self.assertRedirects(response, f'/book/{self.book1.book_id}/', status_code=302,
            target_status_code=200, fetch_redirect_response=True)
    def test_client_access_review_on_logged_in_not_author(self):
        # test client access review on logged in and was not author
        # should can review and redirect to book page
        c = Client()
        c.login(username='user1', password='password')
        post = {
            'title':'review title',
            'message':'review message',
            'score':3,
        }
        response = c.post(f'/book/{self.book2.book_id}/review/', post)
        with self.subTest():
            self.assertRedirects(response, f'/book/{self.book2.book_id}/', status_code=302,
            target_status_code=200, fetch_redirect_response=True)
        with self.subTest():
            self.assertEqual(Review.objects.filter(book_refer=self.book2,reviewer=self.user1).count(),1)
        review = Review.objects.filter(book_refer=self.book2,reviewer=self.user1).last()
        with self.subTest():
            self.assertEqual(review.reviewer,self.user1)
        with self.subTest():
            self.assertEqual(review.book_refer,self.book2)
        with self.subTest():
            self.assertEqual(review.title,'review title')
        with self.subTest():
            self.assertEqual(review.msg, 'review message')
        with self.subTest():
            self.assertEqual(review.score, 3)
    def test_client_access_review_on_logged_in_author(self):
        # client access review on logged in and was author
        # should redirect to book page
        c = Client()
        c.login(username='user2',password='password')
        response = c.get(f'/book/{self.book2.book_id}/review/')
        with self.subTest():
            self.assertRedirects(response, f'/book/{self.book2.book_id}/', status_code=302,
            target_status_code=200, fetch_redirect_response=True)
    def test_client_access_review_no_title(self):
        # client access review not put title
        # should direct to review page
        # get error message
        c = Client()
        c.login(username='user1', password='password')
        post = {
            'message':'review message',
            'score':3,
        }
        response = c.post(f'/book/{self.book2.book_id}/review/', post)
        messages = list(response.context['messages'])
        with self.subTest():
            self.assertEqual(response.status_code,200)
        
        with self.subTest():
            self.assertEqual(len(messages), 1)
        with self.subTest():
            self.assertEqual(str(messages[0]), 'title: This field cannot be null.')
    def test_client_access_review_no_message(self):
        # client access review not put message
        # should direct to review page
        # get error message
        c = Client()
        c.login(username='user1', password='password')
        post = {
            'title':'review title',
            
            'score':3,
        }
        response = c.post(f'/book/{self.book2.book_id}/review/', post)
        messages = list(response.context['messages'])
        with self.subTest():
            self.assertEqual(response.status_code,200)
        with self.subTest():
            self.assertEqual(len(messages), 1)
        with self.subTest():
            self.assertEqual(str(messages[0]), 'msg: This field cannot be null.')
    def test_client_access_review_no_score(self):
        # client access review not put score
        # should direct to review page
        # get error message
        c = Client()
        c.login(username='user3', password='password')
        post = {
            'title':'review title',
            'message':'review message',
        }
        response = c.post(f'/book/{self.book2.book_id}/review/', post)
        with self.subTest():
            self.assertRedirects(response, f'/book/{self.book2.book_id}/', status_code=302,
            target_status_code=200, fetch_redirect_response=True)
        review = Review.objects.filter(reviewer=self.user3,book_refer=self.book2).last()

        with self.subTest():
            self.assertEqual(review.reviewer, self.user3)
        with self.subTest():
            self.assertEqual(review.book_refer,self.book2)
        with self.subTest():
            self.assertEqual(review.score,0)
        with self.subTest():
            self.assertEqual(review.title,'review title')
        with self.subTest():
            self.assertEqual(review.msg, 'review message')