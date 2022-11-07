from django.urls import include, path
from . import views

app_name = "MAIN_APP"
urlpatterns = [
    path('', views.index, name='home'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('sign_in/', include('login_logout.urls')),
    path('about/', views.about, name='about'),
    path('book/', views.book, name='book'),
    path('book/create_book', views.create_book, name='crt_book'),
    path('search/', views.searchbar, name='search'),
    path('testing/', views.testing, name='testing'),
    path('menu/', views.menu, name='menu'),
]
