from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import ProblemSerializer, CommentSerializer, ReplySerializer
from .models import Reply, Comment, Problem
from main.permissions import IsAuthorPermission
from rest_framework import filters as rest_filters
from django_filters import rest_framework as filters

class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated]
        elif self.action in ['update', 'partical_update', ]:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = []

        return [permission() for permission in permissions]

class ProblemViewset(PermissionMixin, ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    # permission_classes = [IsAuthenticated]

    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter
    ]
    filterset_fields = ['author', 'replies']
    search_fields = ['title', 'description']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


class ReplyViewset(PermissionMixin, ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    # permission_classes = [IsAuthenticated]

    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter
    ]
    filterset_fields = ['author', 'created' ]
    search_fields = ['text', ]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


class CommentViewset(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter
    ]
    filterset_fields = ['created', 'author']
    search_fields = ['text', ]

    # permission_classes = [IsAuthenticated]