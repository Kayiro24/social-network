from rest_framework.permissions import BasePermission

class RoleBasedPermission(BasePermission):
    role_permissions = {
        'admin': ['list', 'add_friend', 'search_friend', 'retrieve', 'partial_update'],
        'write': ['list', 'add_friend', 'search_friend', 'retrieve', 'partial_update'],
        'read': ['list', 'search_friend', 'retrieve'],
    }

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_role = request.user.role
        if user_role not in self.role_permissions:
            return False
        
        return view.action in self.role_permissions[user_role]
