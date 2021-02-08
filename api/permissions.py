from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsStudent(BasePermission):
    def has_permission(self,request,view):
        return (request.user.is_student)
class IsInstructor(BasePermission):
    def has_permission(self,request,view):
        return (request.user.is_instructor)