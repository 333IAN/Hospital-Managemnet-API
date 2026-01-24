from rest_framework import serializers
from .models import Invoice, InvoiceItem, Payment, PaymentMode

class PaymentModeSerializer(serializers.ModelSerializer):
    class Meta:
        model=PaymentMode
        fields=['id', 'name']

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=InvoiceItem
        fields=['id', 'item_name', 'quantity', 'unit_price', 'total_price']

class PaymentSerializer(serializers.ModelSerializer):
    payment_mode_name=serializers.CharField(source='payment_mode.name', read_only=True)
    class Meta:
        model=Payment
        fields=['id', 'payment_mode', 'payment_mode_name', 'amount', 'transaction_id', 'payment_date', 'recorded_by']
        read_only_fields=['recorded_by', 'payment_date']

class InvoiceSerializer(serializers.ModelSerializer):
    items=InvoiceItemSerializer(many=True, read_only=True)
    payments=PaymentSerializer(many=True, read_only=True)

    patient_name=serializers.CharField(source='patient.user.first_name', read_only=True)

    class Meta:
        model=Invoice
        fields=['id', 'patient', 'patient_name', 'appointment', 'invoice_date', 'due_date', 'total_amount', 'paid_amount', 'status', 'items', 'payments']
        read_only_fields=['total_amount', 'paid_amount', 'status', 'invoice_date']
        