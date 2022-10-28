from django.contrib import admin

from .models import Registered, Quota, Subject


admin.site.register(CustomAccountManager)
admin.site.register(User)
