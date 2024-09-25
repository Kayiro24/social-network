from django.urls import re_path, include
from .views import AccountModelViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register("", AccountModelViewSet, basename='user')

urlpatterns = [
    re_path("", include(router.urls))
]