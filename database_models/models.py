from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import random as rand

class CustomAccountManager(BaseUserManager):

    def create_user(self, username, email, password, **other_fields):
        
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(user_id=user_id_gen(), username=username, email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password, **other_fields):
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Admin must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Admin must be assigned to is_superuser=True.')
        
        return self.create_user(username, email, password, **other_fields)
    
def user_id_gen():
    rand_id = hex(rand.randint(0, pow(16, 8)))
    while len(User.objects.filter(pk=rand_id)) != 0:
        rand_id = hex(rand.randint(0, pow(16, 8))) 
    return rand_id

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.TextField(primary_key=True, max_length=10, default=0)
    username = models.CharField(unique=True, max_length=32)
    email = models.EmailField(_('Email'), unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    gender = models.CharField(max_length=16, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    occupation = models.CharField(max_length=32, null=True, blank=True)
    bio = models.CharField(_('bio'), blank=True, max_length=300)
    social_link = models.TextField(null=True, blank=True)
    donation_link = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profile_pic/" + str(username), null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def get_username(self):
        return self.username
    def get_about_self(self):
        return (self.gender, self.age, self.occupation)
    def get_bio(self):
        return self.bio
    def get_links(self):
        return (self.social_link, self.donation_link)
    def get_profile_pic(self):
        return self.profile_pic

    def __str__(self):
        return str(self.user_id) + ": " + str(self.username)

def user_id_gen():
    rand_id = hex(rand.randint(0, pow(16, 8)))
    while len(User.objects.filter(pk=rand_id)) != 0:
        rand_id = hex(rand.randint(0, pow(16, 8))) 
    return rand_id
 
class Genre(models.Model):
    genre_list = models.CharField(primary_key=True, max_length=20)

class Book(models.Model):

    book_id = models.TextField(primary_key=True)
    book_name = models.CharField(max_length=60,default='Untitled')
    description = models.CharField(max_length=120, blank=True)
    date_created = models.DateField(default=timezone.now)
    book_type = models.IntegerField(default=1)
    genres = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True)
    author = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    thumbnail = models.ImageField(upload_to="book/" + str(book_id), blank=True, null=True)
    pdf_files = models.FileField(upload_to="book/" + str(book_id) + "/pdfs", blank=True, null=True)

    def get_book_name(self):
        return self.book_name
    def get_description(self):
        return self.description
    def get_date_created(self):
        return self.date_created
    def get_book_type(self):
        return self.book_type
    def get_genres(self):
        return self.genres
    def get_author(self):
        return self.author
    def get_thumbnail(self):
        return self.thumbnail
    def get_pdf_files(self):
        return self.pdf_files
    def get_reviews(self):
        return Review.objects.filter(book_refer=self)
    def get_issues(self):
        return Issue.objects.filter(book_refer=self)
    def get_favorite_books(self):
        return Favorite.objects.filter(user_refer=self)
    
    def get_avg_score(self):
        book_reviews = Review.objects.filter(book_refer=self)
        score_sum = 0
        for review in book_reviews:
            score_sum += review.get_score()
        return score_sum / len(book_reviews)
        

    def __str__(self):
        return str(self.book_id) + ": " + str(self.book_name)

class Favorite(models.Model):
    user_refer = models.OneToOneField(User, on_delete=models.CASCADE)
    book_refer = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)

class Review(models.Model):
    reviewer = models.OneToOneField(User, on_delete=models.CASCADE)
    book_refer = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    review_date = models.DateField(default=timezone.now)
    score = models.FloatField()
    title = models.CharField(max_length=40)
    msg = models.CharField(max_length=500)

    def get_reviewer(self):
        return self.reviewer
    def get_book(self):
        return self.book_refer
    def get_score(self):
        return self.score
    def get_title(self):
        return self.title
    def get_msg(self):
        return self.msg

class Issue(models.Model):
    issuer = models.OneToOneField(User, on_delete=models.CASCADE)
    book_refer = models.ForeignKey(Book, models.SET_NULL, blank=True, null=True)
    issue_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=40)
    msg = models.CharField(max_length=500)

    def get_issuer(self):
        return self.issuer
    def get_book_refer(self):
        return self.book_refer
    def get_attribs(self):
        return (self.issue_date, self.title, self.msg)

class Report(models.Model):
    reporter = models.OneToOneField(User, on_delete=models.CASCADE)
    book_refer = models.ForeignKey(Book, models.SET_NULL, blank=True, null=True)
    report_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=40)
    msg = models.CharField(max_length=100, blank=True)

    def get_reporter(self):
        return self.issuer
    def get_book_refer(self):
        return self.book_refer
    def get_attribs(self):
        return (self.issue_date, self.title, self.msg)

