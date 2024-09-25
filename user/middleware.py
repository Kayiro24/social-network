from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class AccountAuthHelper:

    @staticmethod
    def login_success_response(instance):
        token, refresh_token = instance.get_tokens()

        data = {
            "access_token": token,
            "refresh_token": refresh_token,
        }

        return data

    @staticmethod
    def refresh_token(old_refresh_token):
        from rest_framework_simplejwt.exceptions import TokenError

        try:
            refresh = RefreshToken(old_refresh_token)
            access_token = str(refresh.access_token)
            refresh.set_jti()
            refresh.set_exp()
            refresh_token = str(refresh)
        except TokenError:
            raise ValidationError({"message": 'Token is blacklisted'})

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
