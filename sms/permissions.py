from rest_framework import permissions 

class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 1:
            print(request.user.role)
            return True  # Grant all permissions for teachers
        elif request.user.role == 2 and request.method == 'GET':
            return True  # Allow GET request for students
        return False