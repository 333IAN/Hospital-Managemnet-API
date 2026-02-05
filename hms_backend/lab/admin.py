from django.contrib import admin
from .models import LabTestProfile, LabRequest, LabResult

@admin.register(LabTestProfile)
class LabTestProfileAdmin(admin.ModelAdmin):
    list_display=('name', 'category', 'base_price', 'normal_range')
    search_fields=('name',)


@admin.register(LabRequest)
class LabRequestAdmin(admin.ModelAdmin):
    list_display=('patient', 'test_type', 'status', 'requested_at')
    list_filter=('status',)
    autocomplete_fields=['patient', 'doctor']


@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display=('request', 'result_value', 'is_abnormal', 'completed_at')


