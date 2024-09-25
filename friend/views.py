from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError, MethodNotAllowed
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from core.views import ModelPaginationViewSet
from friend.models import FriendRecord
from friend.permissions import RoleBasedPermission
from friend.serializers import FriendRecordSerializer
from user.models import User
from user.serializers import UserSerializer
from friend.throttling import FriendRequestThrottle
from django.db import transaction


class FriendRecordViewSet(ModelPaginationViewSet, ModelViewSet):
    queryset = FriendRecord.objects.none()
    permission_classes = [RoleBasedPermission]
    serializer_class = FriendRecordSerializer
    search_fields = ['name', 'phone']
    filterset_fields = {
        'status': ['exact'],
    }
    
    def get_queryset(self):
        """
        Retrieves the queryset of friend records for the current user.

        This method filters the FriendRecord model to return only those records
        where the current user is the initiating user. This allows for user-specific
        access to their friendship data.
        
        Filters are: ['requested', 'pending', 'accepted', 'rejected', 'removed', 'blocked', 'un_block']

        Returns:
            QuerySet: A queryset containing FriendRecord instances associated
            with the current user.
        """
        
        return FriendRecord.objects.filter(user=self.user)
    
    @action(
        detail=False,
        methods=["post"],
        url_path="add-friend",
        throttle_classes=[FriendRequestThrottle]
    )
    def add_friend(self, request, *args, **kwargs):
        print("lmoooooo000000000000lma0000000000")
        """
        Send a friend request to a user.

        This method allows the authenticated user to send a friend request 
        to another user specified by the 'friend_id'. It checks if the 
        friend request can be sent based on the current status of the 
        relationship and whether a pending request already exists.

        Parameters:
        - request: The HTTP request object containing the 'friend_id' in the body.
        - *args: Additional positional arguments.
        - **kwargs: Additional keyword arguments.

        Raises:
        - ValidationError: If 'friend_id' is missing, if the user with the given ID 
        does not exist, or if a friend request cannot be sent.

        Returns:
        - Response: A JSON response confirming that the friend request was sent 
        successfully or detailing why it could not be sent.
        """
    
        request = request.data
        
        friend_id = request.get('friend_id')
        if not friend_id:
            raise ValidationError({'message': 'Friend ID is required to add a friend.'})
        
        try:
            friend_instance = User.objects.get(id=friend_id)
        except User.DoesNotExist:
            raise ValidationError({'message': 'User with this ID does not exist.'})
        
        try:
            with transaction.atomic():
                friend_record_instance, created = FriendRecord.objects.get_or_create(
                    user=self.user,
                    friend=friend_instance
                )
                
                if not created and friend_record_instance.status == FriendRecord.StatusTypeChoice.REJECTED:
                    from datetime import timedelta
                    from django.utils import timezone

                    time_since_rejection = timezone.now() - friend_record_instance.created
                    if time_since_rejection < timedelta(hours=24):
                        remaining_time = timedelta(hours=24) - time_since_rejection
                        raise ValidationError({
                            'message': f'Please wait {remaining_time.seconds // 3600} hours and {(remaining_time.seconds % 3600) // 60} minutes before sending another request.'
                        })
                if created:
                    # Create a reciprocal FriendRecord for the friend in a pending state
                    FriendRecord.objects.get_or_create(
                        friend=self.user,
                        user=friend_instance,
                        status=FriendRecord.StatusTypeChoice.PENDING
                    )
                
                friend_record_instance.status = FriendRecord.StatusTypeChoice.REQUESTED
                friend_record_instance.save()
                
                return Response({"message": "Friend request sent successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            raise ValidationError({'message': e})
    
    @action(
        detail=False,
        methods=["get"],
        url_path="search-friend",
    )
    def search_friend(self, request, *args, **kwargs):
        """
        Search for friends based on a query string.

        This method retrieves users whose names or email addresses contain
        the provided query string, excluding the current user and any
        users who are blocked by the current user.

        Parameters:
        - request: The HTTP request object containing query parameters.
        - *args: Additional positional arguments.
        - **kwargs: Additional keyword arguments.

        Raises:
        - ValidationError: If the 'query' parameter is not provided.

        Returns:
        - Response: A JSON response containing a list of non-blocked users
        matching the search criteria, with fields: id, name, email, and username.
        """
    
        query = request.query_params.get('query', None)
        if not query:
            raise ValidationError({'messasge: Parameter is required to search.'})
        
        searched_users = User.objects.filter(
            Q(name__icontains=query) | 
            Q(email__icontains=query)
        ).exclude(id=self.user.id)
        
        non_blocked_users = []
        for searched_user in searched_users:
            if not FriendRecord.objects.filter(
                user=searched_user, friend=self.user, status=FriendRecord.StatusTypeChoice.BLOCKED
            ).exists():
                non_blocked_users.append(searched_user)

        serialized_users = UserSerializer(
            non_blocked_users, fields=['id', 'name', 'email', 'username'], many=True
        ).data

        return Response(serialized_users, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates the status of a friend record.

        Validates the incoming request data and updates the status of a 
        friendship based on various conditions. The possible status values
        are determined by the FriendRecord.StatusTypeChoice enumeration.

        Args:
            request: The HTTP request object containing the data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Raises:
            ValidationError: If the provided status is invalid or if the
            update violates friendship rules.

        Returns:
            Response: A response containing the updated friend record data.
        """
        
        instance = self.get_object()
        
        request = request.data
        friend_status = request.get('status')
        
        if not friend_status:
            raise ValidationError({'message': 'status is required. '})
        elif friend_status and friend_status not in FriendRecord.StatusTypeChoice.values:
            raise ValidationError({'message': f"Invalid status, choose from {FriendRecord.StatusTypeChoice.values}"})
        elif friend_status in [FriendRecord.StatusTypeChoice.ACCEPTED, FriendRecord.StatusTypeChoice.REJECTED] and instance.status != FriendRecord.StatusTypeChoice.PENDING:
            raise ValidationError({'message': 'User cannot accept friend request if it is not being sent by anyone i.e. pending state.'})
        elif friend_status == FriendRecord.StatusTypeChoice.REMOVED and instance.status != FriendRecord.StatusTypeChoice.ACCEPTED:
            raise ValidationError({'message': 'User cannot remove any user if that is not their friend.'})
        elif friend_status == FriendRecord.StatusTypeChoice.UN_BLOCK and instance.status != FriendRecord.StatusTypeChoice.BLOCKED:
            raise ValidationError({'message': 'User cannot unblock if user is not blocked.'})
        
        instance.status = friend_status
        instance.save()
        
        FriendRecord.objects.filter(user=instance.friend, friend=instance.user).update(status=FriendRecord.StatusTypeChoice.ACCEPTED)
        
        return Response(
            FriendRecordSerializer(instance, exclude=['user_details', 'friend_details']).data,
            status=status.HTTP_200_OK
        )    
    
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)
