from rest_framework import serializers
from core.serializers import BaseSerializer
from user.models import User
from user.validators import Validators


class UserSerializer(BaseSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = '__all__'

    def validate_password(self, value):
        Validators.validate_password(value)
        return value
