from rest_framework import permissions
from main.models import Course


class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_instructor


class IsOwnerOrInstructor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Course):
            return obj.instructor == request.user or request.user.is_instructor
        return False


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_instructor
