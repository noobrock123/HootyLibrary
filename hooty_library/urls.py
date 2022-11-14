"""hooty_library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponseNotFound

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('userProfile.urls')),
    path('registeration/', include('register.urls')),
    path('user_profile/', include('userProfile.urls')),
    path('', include('MAIN_APP.urls')),
    path('',include('book_views.urls')),
    path('',include('login_via_google.urls')),
    path('accounts/', include('allauth.urls')),
    path('/<str:others>',HttpResponseNotFound), # in case 404
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
