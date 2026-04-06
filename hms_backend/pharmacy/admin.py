from django.contrib import admin
from .models import Medication, Stock, Prescription

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display=('name', 'category', 'form', 'strength', 'unit_price')
    search_fields=('name',)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display=('medication', 'batch_number', 'expiry_date', 'quantity_in_stock', 'reorder_level')
    list_filter=('expiry_date',)


    def get_queryset(self,request):
        return super().get_queryset(request)
    

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display=('patient', 'medication', 'doctor', 'date_prescribed', 'status')
    list_filter=('status', 'date_prescribed')








# Register your models here.
