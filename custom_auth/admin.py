from django.contrib import admin
from .models import *


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    pass
