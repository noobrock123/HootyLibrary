from django.contrib import admin

from database_models.models import User, CustomAccountManager


admin.site.register(CustomAccountManager)
admin.site.register(User)
