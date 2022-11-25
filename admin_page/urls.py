from django.urls import include, path
from django.contrib import admin
from . import views

app_name = "admin_page"
urlpatterns = [
    path('', views.show_admin_page, name='admin_page' ),
    path('admin_django/', admin.site.urls),
]