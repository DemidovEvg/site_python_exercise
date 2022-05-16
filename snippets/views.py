from django.contrib.auth import get_user_model
from rest_framework import permissions, renderers
from rest_framework.decorators import api_view, action
from rest_framework.generics import (GenericAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import *
from .permissions import *
from .serializers import *

from rest_framework import viewsets
import django_filters.rest_framework

# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'users': reverse('user-list', request=request, format=format),
#         'snippets': reverse('snippet-list', request=request, format=format)
#     })


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    ReadOnlyModelViewSet автоматически добавляет метод list и retrieve
    '''
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        print(request.auth)
        return super().list(request, *args, **kwargs)


class SnippetViewSet(viewsets.ModelViewSet):
    '''
    ModelViewSet автоматически добавляет методы list, create, retrive, update, destroy
    '''
    queryset = Snippet.objects.all()

    serializer_class = SnippetSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('owner', )
    search_fields = ('title', )
    ordering_fields = ('title',)

    # Дополнительная пользовательская точка. По умолчанию только на GET.
    # По умолчанию URL по имени метода.

    def list(self, request, *args, **kwargs):
        print(request.auth)
        return super().list(request, *args, **kwargs)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
