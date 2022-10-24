from django.urls import include, path
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('registeration/', include('register.urls'))
]