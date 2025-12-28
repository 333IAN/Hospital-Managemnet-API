from django.contrib import admin
from .models import Vitals, Consultation, Prescription, PrescriptionItem, LabRequest, Appointment

class PrescriptionItemInLine(admin.TabularInline):
    model=PrescriptionItem
    extra=1

class PrescriptionAdmin(admin.ModelAdmin):
    inlines= [PrescriptionItemInLine]
    list_display = ('patient', 'doctor', 'date_prescribed', 'is_dispensed')
    list_filter = ('is_dispensed', 'date_prescribed')


admin.site.register(Appointment)
admin.site.register(Vitals)
admin.site.register(Consultation)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(LabRequest)



# Register your models here.
