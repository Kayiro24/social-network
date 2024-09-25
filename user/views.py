from django.db import IntegrityError, transaction
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError, MethodNotAllowed
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny, IsAuthenticated

from user.methods import generate_username
from user.middleware import AccountAuthHelper
from user.models import User
from user.serializers import UserSerializer
from user.validators import Validators


class AccountModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'add_friend', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
            
    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)
    
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)
    
    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)
    
    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)

    def create(self, request, *args, **kwargs):
        data = request.data
        data['username'] = generate_username()

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        
        try:
            with transaction.atomic():
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'] )
                self.perform_create(serializer)
                
                data = AccountAuthHelper.login_success_response(serializer.instance)
                data['message'] = f"User with email {serializer.instance.email} created successfully."
                data['user_id'] = serializer.instance.id
        except IntegrityError:
            raise ValidationError({'message': 'User with this email already exists.'})
        
        return Response(data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=['post'],
        url_path='login'
    )
    def login(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        Validators.validate_password(validated_data['password'])

        try:
            user_instance = User.objects.get(email=validated_data['email'])
        except User.DoesNotExist:
            raise ValidationError({'message': 'User with this email does not exists.'})

        if not user_instance.check_password(data['password']):
            raise ValidationError({'message': 'Invalid password.'})
        
        data = AccountAuthHelper.login_success_response(user_instance)
        data['message'] = "Login successful."
        data['user_id'] = user_instance.id

        return Response(data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post"],
        url_path="token/refresh",
    )
    def refresh_token(self, request, *args, **kwargs):
        """
        Refresh an authentication token using a valid refresh token.

        This method accepts a refresh token and returns a new access token
        and refresh token if the provided refresh token is valid. The
        client must send the refresh token as a query parameter.

        Parameters:
        - request: The HTTP request object containing the 'refresh_token' 
        in the query parameters.
        - *args: Additional positional arguments.
        - **kwargs: Additional keyword arguments.

        Raises:
        - ValidationError: If the 'refresh_token' is missing or invalid.

        Returns:
        - Response: A JSON response containing the new access token, 
        or an error message if the refresh token is not valid.
        """
        old_refresh_token = request.query_params.get('refresh_token')
        if old_refresh_token is None:
            raise ValidationError({'message': 'Refresh Token is required.'})
        
        return Response(AccountAuthHelper.refresh_token(old_refresh_token), status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific object and return its serialized data.

        This method fetches the instance of the object specified by the 
        URL parameters and serializes it to return a JSON response 
        containing the object's details.

        Parameters:
        - request: The HTTP request object.
        - *args: Additional positional arguments.
        - **kwargs: Additional keyword arguments.

        Returns:
        - Response: A JSON response containing the serialized data of the 
        requested object, including the fields: id, username, name, email, 
        created, and modified.
        """
        instance = self.get_object()

        serializer = self.get_serializer(
            instance, fields=['id', 'username', 'name', 'email', 'created', 'modified']
        )
        return Response(serializer.data)
