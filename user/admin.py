from django.contrib import admin
from core.admin import CreationModificationBaseAdmin
from user.models import User


@admin.register(User)
class UserAdmin(CreationModificationBaseAdmin):
    list_display = ['email', 'name', 'username', 'role']
    search_fields = ['name', 'username', 'email']
