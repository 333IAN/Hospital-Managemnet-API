from django.db import models

from users.models import PatientProfile, DoctorProfile, User


class LabTestProfile(models.Model):
    name=models.CharField(max_length=255)
    category=models.CharField(max_length=100, help_text="e.g., Hematology, Biochemistry")
    base_price=models.DecimalField(max_digits=10, decimal_places=2)
    normal_range=models.CharField(max_length=255, help_text="e.g., 13.5-17.5 g/dL")
    unit=models.CharField(max_length=50, help_text="e.g., g/dL, mg/dL")

    def __str__(self):
        return self.name
    

class LabRequest(models.Model):
    STATUS_CHOICES=[
        ('PENDING', 'Pending'),
        ('COLLECTED', 'Sample Collected'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    patient=models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='lab_requests')
    doctor=models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='lab_orders')
    test_type=models.ForeignKey(LabTestProfile, on_delete=models.PROTECT)
    requested_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    clinical_note=models.TextField(blank=True, help_text="Doctor's notes for the lab tech")

    def __str__(self):
        return f"{self.test_type.name} for {self.patient.user.last_name}"
    

class LabResult(models.Model):
    request=models.OneToOneField(LabRequest, on_delete=models.CASCADE, related_name= 'result')
    lab_tech=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'LAB_TECH'})
    result_value=models.CharField(max_length=255)
    is_abnormal=models.BooleanField(default=False)
    technician_remarks=models.TextField(blank=True)
    completed_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Result for {self.request.test_type.name}"
    


# Create your models here.
