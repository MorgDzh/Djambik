from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import ProblemSerializer, CommentSerializer, ReplySerializer, FavoriteSerializer, \
    RatingSerializer
from .models import Reply, Comment, Problem, Favorite, Rating
from main.permissions import IsAuthorPermission
from rest_framework import filters as rest_filters, viewsets
from django_filters import rest_framework as filters
from likes.mixins import LikedMixin

class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated]
        elif self.action in ['update', 'partical_update', 'destroy']:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = []

        return [permission() for permission in permissions]

class ProblemViewset(PermissionMixin, ModelViewSet, LikedMixin):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = [IsAuthenticated]

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


class FavoriteViewset(PermissionMixin, ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]


class ReplyViewset(PermissionMixin, ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

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

    permission_classes = [IsAuthenticated]


class RatingViewset(PermissionMixin, viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {
            'request': self.request
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    filterset_fields = ['rating']
    search_fields = ['problem']