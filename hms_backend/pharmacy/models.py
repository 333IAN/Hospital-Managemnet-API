from django.db import models

from django.utils import timezone
from users.models import User, PatientProfile, DoctorProfile

class Medication(models.Model):
    name=models.CharField(max_length=255)
    category=models.CharField(max_length=100)
    form=models.CharField(max_length=50)
    strength=models.CharField(max_length=50)
    unit_price=models.DecimalField(max_digits=10, decimal_places=2)
    description=models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.strength})"
    

class Stock(models.Model):
    medication=models.ForeignKey(Medication, on_delete=models.CASCADE, related_name= 'stocks')
    batch_number=models.CharField(max_length=100, unique=True)
    expiry_date=models.DateField()
    quantity_in_stock=models.PositiveIntegerField(default=0)
    reorder_level=models.PositiveIntegerField(default=10)

    def is_expired(self):
        return self.expiry_date < timezone.now().date()
    
    def __str__(self):
        return f"{self.medication.name} - Batch: {self.batch_number} ({self.quantity_in_stock} left)"
    
class Prescription(models.Model):
    STATUS_CHOICES=[
        ('PENDING', 'Pending'),
        ('DISPENSED', 'Dispensed'),
        ('CANCELLED', 'Cancelled'),
    ]

    patient=models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='prescriptions')
    doctor=models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='prescribed_by')
    medication=models.ForeignKey(Medication, on_delete=models.CASCADE)

    dosage=models.CharField(max_length=255)
    frequency=models.CharField(max_length=255)
    duration=models.CharField(max_length=255)

    date_prescribed=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default= 'PENDING')
    notes=models.TextField(blank=True)

    def __str__(self):
        return f"RX for {self.patient.user.last_name}: {self.medication.name}"
    


# Create your models here.
