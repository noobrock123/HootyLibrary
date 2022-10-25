from django.urls import include, path
from . import views

app_name = "MAIN_APP"
urlpatterns = [
    path('', views.index, name='home'),
    path('registeration/', include('register.urls')),
    path('about/', views.about, name='about')
]