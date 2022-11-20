from django.urls import include, path
from . import views

app_name = "book_views"
urlpatterns = [

    #path('book/create_book/', views.create_book, name='create_book'),
    #path('book/<str:book_id>/pdf/', views.book_pdf, name='book_pdf'),
    #path('book/<str:book_id>/thumbnail/',views.book_thumbnail, name='book_thumbnail'),
    #path('book/<str:book_id>/', views.book_views, name='book'),
    #path('book/<str:book_id>/review/', views.review, name='review'),
    #path('book/<str:book_id>/report/', views.report, name='report'),
    #path('book/<str:book_id>/book_favorite/', views.book_favorite, name='book_favorite'),
    #path('book/<str:book_id>/issue/', views.issue, name='issue'),
    path('create_book', views.create_book, name='create_book'),
    path('pdf/<str:book_id>', views.book_pdf, name='book_pdf'),
    path('thumbnail/<str:book_id>/',views.book_thumbnail, name='book_thumbnail'),
    path('<str:book_id>', views.book_views, name='book'),
    path('', include('messaging.urls')),
    
]