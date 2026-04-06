from django.contrib import admin

from .models import Invoice, InvoiceItem, Payment, PaymentMode

class InvoiceItemInLine(admin.TabularInline):
    model=InvoiceItem
    extra=1

class PaymentInLine(admin.TabularInline):
    model=Payment
    extra=1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display=('id', 'patient', 'status', 'total_amount', 'paid_amount', 'invoice_date')
    inlines=[InvoiceItemInLine, PaymentInLine]
    list_filter=('status', 'invoice_date')

admin.site.register(PaymentMode)
admin.site.register(Payment)