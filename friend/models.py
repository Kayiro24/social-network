from django.db import models
from core.models import CreationModificationBase
from user.models import User


class FriendRecord(CreationModificationBase):
    class StatusTypeChoice(models.TextChoices):
        REQUESTED = 'requested'
        PENDING = 'pending'
        ACCEPTED = 'accepted'
        REJECTED = 'rejected'
        REMOVED = 'removed'
        BLOCKED = 'blocked'
        UN_BLOCK = 'un_block'
    
    user = models.ForeignKey(User, related_name='_user', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='_friend_user', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=StatusTypeChoice.choices, default=StatusTypeChoice.PENDING, db_index=True
    )

    class Meta:
        unique_together = ('user', 'friend')