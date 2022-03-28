from django.urls import path
from .views import *


app_name = 'custom_auth'

urlpatterns = [
    path('registration/',
         RegistrationUserView.as_view(),
         name='registration'),

    path('login/vk/',
         login_vk,
         name='login_vk'),

    path('login/<str:error>',
         CustomLoginView.as_view(),
         name='login_error'),

    path('login/',
         CustomLoginView.as_view(),
         name='login'),

    path('logout/',
         CustomLogoutView.as_view(),
         name='logout'),

    path('password_reset/',
         CustomPasswordResetView.as_view(),
         name='password_reset'),

    path('reset/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('reset/done/',
         CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('reset/complete/',
         CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

]
