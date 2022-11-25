from django.urls import include, path
from . import views

app_name = "MAIN_APP"
urlpatterns = [
    path('', views.index, name='home'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('sign_in/', include('login_logout.urls')),
    path('about/', views.about, name='about'),
    #path('book/', views.book, name='book'),
    #path('search/', views.searchbar, name='search'),
    path('book/create_book', views.create_book, name='crt_book'),
    path('Undiscovered/', views.Undiscovered, name='Undiscovered'),
    path('Popular_today/', views.Popular_today, name='Popular_today'),
    path('Popular_week/', views.Popular_week, name='Popular_week'),
    path('Highest_rating_today/', views.Highest_rating_today, name='Highest_rating_today'),
    path('Highest_rating_week/', views.Highest_rating_week, name='Highest_rating_week'),
    path('Recently/', views.Recently, name='Recently'),
]
