from core.serializers import BaseSerializer
from friend.models import FriendRecord
from user.serializers import UserSerializer


class FriendRecordSerializer(BaseSerializer):
    user_details = UserSerializer(source='user', fields=['name', 'email', 'username'])
    friend_details = UserSerializer(source='friend', fields=['name', 'email', 'username'])

    class Meta:
        model = FriendRecord
        fields = '__all__'
