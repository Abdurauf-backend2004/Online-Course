from rest_framework import permissions
from main.models import Course


class IsInstructor(permissions.BasePermission):
    """
    Permission to check if the user is an instructor.
    """
    def has_permission(self, request, view):
        return request.user.is_instructor


class IsOwnerOrInstructor(permissions.BasePermission):
    """
    Custom permission to allow access to users who are either the instructor of a course or the course owner.
    """
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Course):
            return obj.instructor == request.user or request.user.is_instructor
        return False


class IsStudent(permissions.BasePermission):
    """
    Permission to check if the user is a student.
    """
    def has_permission(self, request, view):
        return not request.user.is_instructor
