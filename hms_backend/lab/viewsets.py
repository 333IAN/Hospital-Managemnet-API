from rest_framework import viewsets, permissions
from .models import LabTestProfile, LabRequest, LabResult
from .serializers import LabTestProfileSerializer, LabRequestSerializer, LabResultSerializer
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from rest_framework.decorators import action
from django.conf import settings


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

    @action(detail=True, methods=['get'], url_path='download-report')
    def download_report(self,request,pk=None):
        result_obj=self.get_object()

        context={
            'result':result_obj,
            'base_dir': settings.BASE_DIR
        }
        html_string=render_to_string('lab_report_pdf.html', context)

        pdf=HTML(string=html_string).write_pdf()

        response=HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition']=f'inline; filename="report_{result_obj.id}.pdf"'
        return response




