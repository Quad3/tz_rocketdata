from rest_framework.permissions import BasePermission

class IsEmployee(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.producer != obj:
            return False
        return True