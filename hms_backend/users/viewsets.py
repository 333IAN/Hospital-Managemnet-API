from rest_framework import viewsets, permissions
from .models import User, PatientProfile, DoctorProfile, NurseProfile, PharmacistProfile, LabTechProfile, RadiologistProfile, ReceptionistProfile
from .serializers import UserSerializer, PatientProfileSerializer, DoctorProfileSerializer, NurseProfileSerializer, PharmacistProfileSerializer, LabTechProfileSerializer, RadiologistProfileSerializer, ReceptionistProfileSerializer
from .permissions import IsAdminUser, IsSelfOrAdmin, IsReceptionistOrAdmin

class UserViewSet(viewsets.ModelViewSet):
    serializer_class=UserSerializer
    permission_classes=[permissions.IsAuthenticated, IsSelfOrAdmin]

    def get_queryset(self):
        user=self.request.user
        if user.role=='ADMIN':
            return User.objects.all()
        return User.objects.filter(id=user.id)
    

class PatientProfileViewSet(viewsets.ModelViewSet):
    query_set=PatientProfile.objects.all()
    serializer_class=PatientProfileSerializer
    permission_classes=[permissions.IsAuthenticated, IsReceptionistOrAdmin]

    def get_queryset(self):
        user=self.request.user
        if user.role in ['ADMIN', 'RECEPTIONIST', 'DOCTOR', 'NURSE']:
            return PatientProfile.objects.all()
        return PatientProfile.objects.filter(user=user)
    
class BaseStaffViewSet(viewsets.ModelViewSet):
    permission_classes=[permissions.IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return self.queryset
    
class DoctorProfileViewSet(BaseStaffViewSet):
    queryset=DoctorProfile.objects.all()
    serializer_class=DoctorProfileSerializer
    permission_classes=[permissions.IsAuthenticated]

class NurseProfileViewSet(BaseStaffViewSet):
    queryset=NurseProfile.objects.all()
    serializer_class=NurseProfileSerializer

class PharmacistProfileViewSet(BaseStaffViewSet):
    queryset=PharmacistProfile.objects.all()
    serializer_class=PharmacistProfileSerializer

class LabTechProfileViewSet(BaseStaffViewSet):
    queryset=LabTechProfile.objects.all()
    serializer_class=LabTechProfileSerializer

class RadiologistProfileViewSet(BaseStaffViewSet):  
    queryset=RadiologistProfile.objects.all()
    serializer_class=RadiologistProfileSerializer

class ReceptionistProfileViewSet(BaseStaffViewSet):
    queryset=ReceptionistProfile.objects.all()
    serializer_class=ReceptionistProfileSerializer