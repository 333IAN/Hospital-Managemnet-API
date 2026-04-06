from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'ADMIN')
    
class IsReceptionistOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role in ['RECEPTIONIST', 'ADMIN']
        return False
    
class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role=='ADMIN':
            return True
        return obj==request.user or (hasattr(obj, 'user') and obj.user==request.user)
    
