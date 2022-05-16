from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets.views import *


router = DefaultRouter()
router.register(prefix=r'snippets', viewset=SnippetViewSet, basename='snippet')
router.register(prefix=r'users', viewset=UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls))
]
