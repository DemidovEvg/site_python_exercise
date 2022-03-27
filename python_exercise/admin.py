from django.contrib import admin
from .models import *


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'is_published',
        'category',
        'time_create',
        'time_update')

    list_display_links = ('id', 'title')
    list_editable = ('is_published',)

    fields = ('title',
              'task_text',
              'is_published',
              'category',
              'tag',
              'time_create',
              'author_create',
              'time_update',
              'author_update')

    readonly_fields = ('time_create', 'time_update')

    save_on_top = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'complexity')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}

    list_editable = ('complexity',)

    save_on_top = True


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}

    save_on_top = True


# @admin.register(Commentary)
# class CommentaryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'author', 'time_create', 'exercise')
#     list_display_links = ('id', 'author')

#     save_on_top = True
