from django.urls import re_path, include
from rest_framework import routers

from friend.views import FriendRecordViewSet

router = routers.SimpleRouter()
router.register("", FriendRecordViewSet, basename='friend-record')

urlpatterns = [
    re_path("", include(router.urls))
]