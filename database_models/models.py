from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import random as rand


class CustomAccountManager(BaseUserManager):

    def create_user(self, username, email, password, **other_fields):
        # if len(username) == 0 or len(username) > 32:
        #     raise ValueError(
        #         _('Your username length can not be 0 or more than 32'))
        # try:
        #     validate_email(email)
        # except ValidationError:
        #     raise
        # if not email:
        #     raise ValueError(_('You must provide an email address'))
        # if 'user_id' in other_fields and other_fields['user_id']:
        #     if User.objects.filter(user_id=other_fields['user_id']).exists():
        #         raise ValueError(_('Your user_id already used'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **other_fields)
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


def get_profile_pic_path(instance, file):
    return f"profile_pic/{instance.username}/{file}"


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.TextField(primary_key=True, max_length=12, default=0)
    username = models.CharField(unique=True, max_length=32)
    alias_name = models.CharField(max_length=40, blank=True)
    email = models.EmailField(_('Email'), unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    gender = models.CharField(max_length=16, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    occupation = models.CharField(max_length=32, null=True, blank=True)
    bio = models.TextField(_('bio'), blank=True, max_length=300)
    social_link = models.TextField(null=True, blank=True)
    donation_link = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(
        upload_to=get_profile_pic_path, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # def clean(self) -> None:
    #     if len(self.username) == 0 or len(self.username) > 32:
    #         raise ValueError(
    #             _('Your username length can not be 0 or more than 32'))
    #     try:
    #         validate_email(self.email)
    #     except ValidationError:
    #         raise
    #     if not self.email:
    #         raise ValueError(_('You must provide an email address'))
        # if 'user_id' in self.other_fields and self.other_fields['user_id']:
        #     if User.objects.filter(user_id=self.other_fields['user_id']).exists():
        #         raise ValueError(_('Your user_id already used'))
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save()
    

    

    def get_about_self(self):
        return (self.gender, self.age, self.occupation)

    
    def get_links(self):
        return (self.social_link, self.donation_link)

    

    def __str__(self):
        return str(self.user_id) + ": " + str(self.username)


def pre_save_user_random_id(sender, instance, *args, **kwargs):
    if not instance.user_id:
        klass = instance.__class__
        rand_id = hex(rand.randint(0, pow(16, 8)))
        while klass.objects.filter(pk=rand_id).exists():
            rand_id = hex(rand.randint(0, pow(16, 8)))
        instance.user_id = rand_id


pre_save.connect(pre_save_user_random_id, sender=User)


class Genre(models.Model):
    genre_list = models.CharField(primary_key=True, max_length=20)

    def __str__(self):
        return str(self.genre_list)


def get_thumbnail_path(instance, file):
    return f"book/{instance.book_id}/{file}"


def get_pdf_files_path(instance, file):
    return f"book/{instance.book_id}/pdfs/{file}"


class Book(models.Model):
    book_id = models.CharField(primary_key=True, max_length=10)
    book_name = models.CharField(max_length=60, default='Untitled')
    description = models.TextField(max_length=120, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    book_type = models.IntegerField(default=1)
    genres = models.ManyToManyField(Genre)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    thumbnail = models.ImageField(
        upload_to=get_thumbnail_path, blank=True, null=True)

    pdf_files = models.FileField(
        upload_to=get_pdf_files_path, blank=True, null=True)

    '''
    def __init__(self):
        super(Book, self).__init__()
    '''

    def get_book_id(self):
        return str(self.book_id)

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
        return score_sum / len(book_reviews) if len(book_reviews) != 0 else 0

    def get_views(self):
        book = Read.objects.filter(book_refer=self)
        return book.user_refer.all()

    def save(self, *args, **kwargs):
        rand_id = hex(rand.randint(0, pow(16, 8)))
        while Book.objects.filter(book_id=rand_id).exists():
            rand_id = hex(rand.randint(0, pow(16, 8)))
        self.book_id = rand_id
        super(Book, self).save()

    def __str__(self):
        return str(self.book_id) + ": " + str(self.book_name)


def pre_save_book_random_id(sender, instance, *args, **kwargs):
    if not instance.book_id:
        klass = instance.__class__
        rand_id = hex(rand.randint(0, pow(16, 8)))
        while klass.objects.filter(book_id=rand_id).exists():
            rand_id = hex(rand.randint(0, pow(16, 8)))
        instance.book_id = rand_id


pre_save.connect(pre_save_book_random_id, sender=Book)


class Read(models.Model):
    user_refer = models.ForeignKey(User, on_delete=models.CASCADE)
    book_refer = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_read_latest_time = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user_refer', 'book_refer',)

    def get_recent_read_books(self, user):
        books = self.user_refer.get(user).order_by('-book_read_latest_time')
        return books.book_refer.all()


class Favorite(models.Model):
    user_refer = models.ForeignKey(User, on_delete=models.CASCADE)
    book_refer = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_refer', 'book_refer',)

    def __str__(self) -> str:
        return f"{self.user_refer} -> {self.book_refer} "


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    book_refer = models.ForeignKey(Book, on_delete=models.CASCADE)
    review_date = models.DateTimeField(default=timezone.now)
    score = models.FloatField(default=0)
    title = models.CharField(max_length=40)
    msg = models.TextField(max_length=500)

    is_edited = models.BooleanField(default=False)
    last_edited = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('reviewer', 'book_refer',)

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
    issuer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    book_refer = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=40)
    msg = models.TextField(max_length=500)

    def get_issuer(self):
        return self.issuer

    def get_book_refer(self):
        return self.book_refer

    def get_attribs(self):
        return (self.issue_date, self.title, self.msg)


class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    book_refer = models.ForeignKey(Book, on_delete=models.CASCADE)
    report_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=40)
    msg = models.TextField(max_length=100, blank=True)

    def get_reporter(self):
        return self.issuer

    def get_book_refer(self):
        return self.book_refer

    def get_attribs(self):
        return (self.issue_date, self.title, self.msg)
