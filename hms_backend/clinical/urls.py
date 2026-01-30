from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . viewsets import AppointmentViewSet, VitalsViewSet, PrescriptionViewSet, LabRequestViewSet, ConsultationViewSet

router = DefaultRouter()
router.register('appointments', AppointmentViewSet, basename='appointment')
router.register('vitals', VitalsViewSet, basename='vital')
router.register('consultations', ConsultationViewSet, basename='consultation')
router.register('prescriptions', PrescriptionViewSet, basename='prescription')
router.register('lab-requests', LabRequestViewSet, basename='labrequest')

urlpatterns = [
    path('', include(router.urls)),
]