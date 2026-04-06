from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import UserViewSet, PatientProfileViewSet, DoctorProfileViewSet, NurseProfileViewSet, PharmacistProfileViewSet, LabTechProfileViewSet, RadiologistProfileViewSet, ReceptionistProfileViewSet
router = DefaultRouter()

router.register('accounts', UserViewSet, basename='user')
router.register('patients', PatientProfileViewSet, basename='patient')
router.register('doctors', DoctorProfileViewSet, basename='doctor')
router.register('nurses', NurseProfileViewSet, basename='nurse')
router.register('pharmacists', PharmacistProfileViewSet, basename='pharmacist')
router.register('lab-techs', LabTechProfileViewSet, basename='labtech')
router.register('radiologists', RadiologistProfileViewSet, basename='radiologist')
router.register('receptionists', ReceptionistProfileViewSet, basename='receptionist')


urlpatterns=[
    path('', include(router.urls)),
]