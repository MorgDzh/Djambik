from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from main.views import ProblemViewset, ReplyViewset, CommentViewset, FavoriteViewset

router = DefaultRouter()
router.register('problems', ProblemViewset)
router.register('replies', ReplyViewset)
router.register('comments', CommentViewset)
router.register('favorites', FavoriteViewset)

schema_view = get_schema_view(
   openapi.Info(
      title="djumbik Api",
      default_version='v1',
      description="Gun-selling site \n100% Legal(no)",
      terms_of_service="https://www.google.com/policies/terms/",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include("accounts.urls")),

    # drf-yasg
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

