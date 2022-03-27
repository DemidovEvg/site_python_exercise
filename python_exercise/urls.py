from django.urls import include, path, re_path
from .views import *
from django.views.generic.base import RedirectView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView

app_name = 'python_exercise'

urlpatterns = [
    path('',
         ShowExercises.as_view(),
         name='home'),

    path('tag/<slug:tag_slug>/',
         ShowExercises.as_view(),
         name='tag'),

    path('category/<slug:category_slug>/',
         ShowExercises.as_view(),
         name='category'),

    path('category/<slug:category_slug>/tag/<slug:tag_slug>',
         ShowExercises.as_view(),
         name='category_and_tag'),

    path('create-exercise/',
         CreateExercise.as_view(),
         name='create-exercise'),

    path('create-tag/',
         create_tag,
         name='create-tag'),

    path('update-exercise/<int:exercise_id>/',
         UpdateExercise.as_view(),
         name='update-exercise'),

    path('exercise/<int:exercise_id>/',
         ShowComments.as_view(),
         name='exercise'),

    path('user/exercises/<slug:user_slug>/',
         ShowUserExercises.as_view(),
         name='user_exercises'),

    path('user/exercises/create/<slug:user_slug>/',
         ShowUserExercisesCreate.as_view(),
         name='user_exercises_create'),

    path('user/exercises/update/<slug:user_slug>/',
         ShowUserExercisesUpdate.as_view(),
         name='user_exercises_update'),

]
