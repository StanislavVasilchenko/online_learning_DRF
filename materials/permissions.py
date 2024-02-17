from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    message = 'You are not allowed to moderator'

    def has_permission(self, request, view):
        if request.user.groups.filter(name='moderator').exists():
            return True
        return False


class IsUserIsOwner(permissions.BasePermission):
    message = 'You are not Owner of this object'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
