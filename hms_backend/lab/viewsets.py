from rest_framework import viewsets, permissions
from .models import LabTestProfile, LabRequest, LabResult
from .serializers import LabTestProfileSerializer, LabRequestSerializer, LabResultSerializer


class LabTestProfileViewSet(viewsets.ModelViewSet):
    queryset=LabTestProfile.objects.all()
    serializer_class=LabTestProfileSerializer

class LabRequestViewSet(viewsets.ModelViewSet):
    serializer_class=LabRequestSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        if user.role=='PATIENT':
            return LabRequest.objects.filter(patient__user=user)
        return LabRequest.objects.all()
    
    def perform_create(self, serializer):
        if hasattr(self.request.user, 'doctorprofile'):
            serializer.save(doctor=self.request.user.doctor_profile)
        else:
            serializer.save()


class LabResultViewSet(viewsets.ModelViewSet):
    queryset=LabResult.objects.all()
    serializer_class=LabResultSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(lab_tech=self.request.user)




