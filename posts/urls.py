from django.urls import path, include
from .views import PostListView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('posts/', PostListView.as_view(), name='posts_api'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/docs/', SpectacularRedocView.as_view(url_name='schema'), name='docs'),
   
]
