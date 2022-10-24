from django.urls import include, path
from . import views
<<<<<<< HEAD

app_name = "MAIN_APP"
urlpatterns = [
    path('', views.index, name='home'),
    path('registeration/', include('register.urls')),
    path('about/', views.about, name='about')
=======
urlpatterns = [
    path('', views.index, name='home'),
    path('registeration/', include('register.urls'))
>>>>>>> 6071948 (Linking homepage and make static files)
]