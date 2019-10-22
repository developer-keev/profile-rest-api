from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import HelloAPIView, HelloViewSet, UserProfileViewSet, UserLoginAPIView, UserProfileFeedViewSet

router = DefaultRouter()
router.register("hello-viewset", HelloViewSet, base_name="hello_viewset")
router.register('profile', UserProfileViewSet)
router.register('feed', UserProfileFeedViewSet)

urlpatterns = [
path("hello-view/", HelloAPIView.as_view()),
path('login/', UserLoginAPIView.as_view()),
path("", include(router.urls))
]
