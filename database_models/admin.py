from django.contrib import admin
from .models import CustomAccountManager, User, Genre, Book, Favorite, Review, Issue, Report
from django.contrib.auth.admin import UserAdmin

class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('user_id', 'username', 'email',)
    list_filter = ('is_active', 'is_superuser')
    ordering = ('date_joined',)
    list_display = ('user_id','username', 'email', 'date_joined',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('user_id', 'username', 'email', )}),
        ('Permission', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('gender', 'age', 'occupation')}),
    )

class BookAdminConfig(admin.ModelAdmin):
    model = Book
    search_fields = ('book_id', 'book_name', 'date_created', 'book_type')
    ordering = ('book_id', 'date_created')
    list_display = ('book_id', 'book_name', 'book_type', 'genres','date_created')
    fieldsets = (
        (None, {'fields': ('book_id', 'book_name', 'author')}),
        ('Attributes', {'fields': ('book_type', 'description')}),
        ('Others', {'fields': ('thumbnail', 'pdf_files')})
    )

class GenreAdminConfig(admin.ModelAdmin):
    model = Genre
    list_display = ('genre_list',)
    fieldsets = (
        (None, {'fields': ('genre_list',)}),
    )

class ReviewsAdminConfig(admin.ModelAdmin):
    model = Review
    search_fields = ('reviewer', 'book_refer', 'review_date', 'title')
    ordering = ('reviewer', 'book_refer', 'review_date')
    list_display = ('reviewer', 'book_refer', 'review_date', 'score', 'title')
    fieldsets = (
        ('Reviews', {'fields': ('reviewer', 'book_refer', 'score',
         'title', 'msg')}),
    )

class IssuesAdminView(admin.ModelAdmin):
    model = Issue
    search_fields = ('issuer', 'book_refer', 'issue_date', 'title')
    ordering = ('issuer', 'book_refer', 'issue_date')
    list_display = ('issuer', 'book_refer', 'issue_date', 'title')
    fieldsets = (
        ('Issues', {'fields': ('issuer', 'book_refer', 
         'title', 'msg')}),
    )

class ReportAdmin(admin.ModelAdmin):
    model = Report
    search_fields = ('reporter', 'book_refer', 'report_date', 'title')
    ordering = ('reporter', 'book_refer', 'report_date')
    list_display = ('reporter', 'book_refer', 'report_date', 'title')
    fieldsets = (
        ('Report', {'fields': ('reporter', 'book_refer', 'report_date')}),
        ('Content', {'fields': ('title', 'msg')})
    )


admin.site.register(User, UserAdminConfig)
admin.site.register(Book, BookAdminConfig)
admin.site.register(Genre, GenreAdminConfig)
admin.site.register(Review, ReviewsAdminConfig)
admin.site.register(Issue, IssuesAdminView)
admin.site.register(Report, ReportAdmin)

