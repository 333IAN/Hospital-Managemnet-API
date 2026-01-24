from django.db import models
from users.models import PatientProfile
from clinical.models import Appointment

class PaymentMode(models.Model):
    name=models.CharField(max_length=50, unique=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Invoice(models.Model):
    STATUS_CHOICES=[
        ('PENDING', 'Pending'),
        ('PARTIAL', 'Partial'),
        ('PAID', ' Fully Paid'),
        ('CANCELLED', 'Cancelled'),
    ]

    patient=models.ForeignKey(PatientProfile, on_delete=models.PROTECT, related_name='invoices')
    appointment=models.ForeignKey(Appointment, on_delete=models.SET_NULL, related_name='invoices', null=True, blank=True)

    invoice_date=models.DateTimeField(auto_now_add=True)
    due_date=models.DateField(null=True, blank=True)

    total_amount=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_amount=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"INV-{self.id} | {self.patient.user.first_name}"
    
    def update_totals(self):
        self.paid_amount=sum(payment.amount for payment in self.payments.all())
        if self.paid_amount>=self.total_amount:
            self.status='PAID'
        elif self.paid_amount>0:
            self.status='PARTIAL'
        else:
            self.status='PENDING'
        self.save()

class InvoiceItem(models.Model):
    invoice=models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    item_name=models.CharField(max_length=255)
    quantity=models.PositiveIntegerField(default=1)
    unit_price=models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.unit_price
    
    def save (self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.invoice.total_amount=sum(item.total_price for item in self.invoice.items.all())
        self.invoice.save()


class Payment(models.Model):
    invoice=models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='payments')
    payment_mode=models.ForeignKey(PaymentMode, on_delete=models.PROTECT)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id=models.CharField(max_length=100, blank=True, null=True, unique=True)
    payment_date=models.DateTimeField(auto_now_add=True)
    recorded_by=models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.invoice.update_totals()

    def __str__(self):
        return f"PAY-{self.id} | {self.amount}"
    

    
