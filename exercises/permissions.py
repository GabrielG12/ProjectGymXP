from rest_framework.permissions import BasePermission


class IsExerciseOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username
