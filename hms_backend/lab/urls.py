from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import LabTestProfileViewSet, LabRequestViewSet, LabResultViewSet

router=DefaultRouter()
router.register('tests', LabTestProfileViewSet, basename='lab-test')
router.register('requests', LabRequestViewSet, basename='lab-request')
router.register('results', LabResultViewSet, basename='lab-result')

urlpatterns=[
    path('', include(router.urls)),
]


