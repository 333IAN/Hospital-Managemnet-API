from rest_framework import viewsets, permissions
from .models import Appointment, Vitals, Consultation, Prescription, LabRequest
from .serializers import AppointmentSerializer, VitalsSerializer, ConsultationSerializer, PrescriptionSerializer, LabRequestSerializer
from .permissions import IsDoctor, IsAssignedDoctor, CanViewMedicalRecord, IsNurse, IsPharmacist, IsLabTech

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class=AppointmentSerializer
    permission_classes=[permissions.IsAuthenticated, CanViewMedicalRecord]

    def get_queryset(self):
        user=self.request.user
        if user.role in ['ADMIN', 'RECEPTIONIST']:
            return Appointment.objects.all()
        elif user.role=='DOCTOR':
            return Appointment.objects.filter(doctor__user=user)
        elif user.role=='PATIENT':
            return Appointment.objects.filter(patient__user=user)
        elif user.role=='NURSE':
            return Appointment.objects.filter(status__in=['SCHEDULED', 'ARRIVED', 'IN_CONSULTATION'])
        return Appointment.objects.none()
    
class VitalsViewSet(viewsets.ModelViewSet):
    query_set=Vitals.objects.all()
    serializer_class=VitalsSerializer
    permission_classes=[permissions.IsAuthenticated, IsNurse | IsDoctor ]

    def perform_create(self, serializer):
        if self.request.user.role=='NURSE':
            serializer.save(recorded_by=self.request.user.nurse_profile)
        else:
            serializer.save()

class ConsultationViewSet(viewsets.ModelViewSet):
    query_set=Consultation.objects.all()
    serializer_class=ConsultationSerializer
    permission_classes=[permissions.IsAuthenticated, IsDoctor | IsNurse | CanViewMedicalRecord]

    def get_queryset(self):
        user=self.request.user
        if user.role=='ADMIN':
            return Consultation.objects.all()
        return Consultation.objects.filter(doctor__user=user)
    
class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset=Prescription.objects.all()
    serializer_class=PrescriptionSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        if user.role=='PHARMACIST':
            return Prescription.objects.all()
        elif user.role=='PATIENT':
            return Prescription.objects.filter(patient__user=user)
        return Prescription.objects.all()
    
class LabRequestViewSet(viewsets.ModelViewSet):
    queryset=LabRequest.objects.all()
    serializer_class=LabRequestSerializer
    permission_classes=[permissions.IsAuthenticated, IsLabTech | IsDoctor]