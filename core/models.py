import uuid
from django.db import models


class CreationModificationBase(models.Model):
    """Mixin for adding creation and modification datetime."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(
        auto_now_add=True, help_text="When this instance was created."
    )
    modified = models.DateTimeField(
        auto_now=True, help_text="When this instance was modified."
    )

    class Meta:
        abstract = True

    def update(self, commit=False, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if commit:
            self.save()
