from rest_framework.throttling import SimpleRateThrottle
from rest_framework.exceptions import Throttled

class FriendRequestThrottle(SimpleRateThrottle):
    scope = 'friend_request'

    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            return self.get_ident(request)
        return f'throttle_friend_request_{request.user.id}'
    