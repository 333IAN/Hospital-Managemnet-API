from rest_framework import permissions

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool (request.user.is_authenticated and request.user.role=='DOCTOR')
    
class IsNurse(permissions.BasePermisssion):
    def has_permission(self, request, view):
        return bool (request.user.is_authenticated and request.user.role=='NURSE')
    
class IsPharmacist(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool (request.user.is_authenticated and request.user.role=='PHARMACIST')
    
class IsLabTech(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool (request.user.is_authenticated and request.user.role=='LAB_TECH')
    
class CanViewMedicalRecord(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user=request.user
        if user.role in ['ADMIN', 'DOCTOR', 'NURSE', 'LAB_TECH', 'RADIOLOGIST']:
            return True
        if user.role=='PATIENT':
            return obj.patient.user==user
        return False
    
class IsAssignedDoctor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.doctor.user==request.user