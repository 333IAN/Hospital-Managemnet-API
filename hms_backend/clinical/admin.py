from django.contrib import admin
from .models import Vitals, Consultation, Prescription, PrescriptionItem, LabRequest, Appointment



class PrescriptionItemInLine(admin.TabularInline):
    model=PrescriptionItem
    extra=1

class PrescriptionAdmin(admin.ModelAdmin):
    inlines= [PrescriptionItemInLine]
    list_display = ('patient', 'doctor', 'date_prescribed', 'is_dispensed')
    list_filter = ('is_dispensed', 'date_prescribed')

@admin.register(Vitals)
class VitalsAdmin(admin.ModelAdmin):
    list_display=('patient', 'temperature', 'blood_pressure', 'recorded_at')
    search_fields=('patient__user__last_name', 'patient__patient_id')


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display=('patient', 'doctor', 'diagnosis', 'created_at')
    list_filter=('doctor', 'created_at')
    search_fields=('patient__user__last_name', 'diagnosis')
    autocomplete_fields=['patient', 'doctor']


admin.site.register(Appointment)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(LabRequest)



# Register your models here.
