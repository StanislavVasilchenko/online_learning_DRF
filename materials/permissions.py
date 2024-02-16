from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    message = 'You are not allowed to moderator'

    def has_permission(self, request, view):
        if request.user.groups.filter(name='moderator').exists():
            return True
        return False


class IsStaff(permissions.BasePermission):
    message = 'You are not allowed to staff'

    def has_permission(self, request, view):
        return request.user.is_staff
