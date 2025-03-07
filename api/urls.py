from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import APIRequestLogViewSet

router = DefaultRouter()
router.register(r'api-logs', APIRequestLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
