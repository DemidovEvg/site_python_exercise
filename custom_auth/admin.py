from django.contrib import admin
from .models import *


class UserDataInline(admin.StackedInline):
    model = UserData
    can_delete = False


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = (UserDataInline, )


# @admin.register(UserData)
# class UserDataAdmin(admin.ModelAdmin):
#     pass
