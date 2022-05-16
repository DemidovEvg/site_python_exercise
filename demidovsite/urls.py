from django.contrib import admin
from django.urls import include, path
from .views import *
from python_exercise.views import *

# from rest_framework import routers
# from .views import UserViewSet, GroupViewSet


# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'groups', GroupViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('custom_auth.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', include('python_exercise.urls')),
    path('api-auth',
         include('rest_framework.urls', namespace='rest_framework')),
    path('rest/', include('snippets.urls')),
    path('chat/', include('chat.urls')),
]


# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handler404 = page_not_found
