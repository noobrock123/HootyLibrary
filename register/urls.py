from django.urls import include, path
from . import views

app_name = "register"
urlpatterns = [
    path('sign_up/', views.register, name='regis'),
    path('sign_in/', views.log_in, name='log_in')

]
