from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from .views import TransferViewSet


router = DefaultRouter()
router.register(r'transfer', TransferViewSet, basename='auth')


urlpatterns = [
    url(r'api/', include(router.urls)),
]

