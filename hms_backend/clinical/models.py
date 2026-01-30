from django.db import models
from simple_history.models import HistoricalRecords
from users.models import PatientProfile, DoctorProfile, NurseProfile, ReceptionistProfile, PharmacistProfile, LabTechProfile

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('ARRIVED', 'Arrived'),
        ('IN_CONSULTATION', 'In Consultation'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    booked_by=models.ForeignKey(ReceptionistProfile, on_delete=models.SET_NULL, null=True, blank=True)
    appointment_date = models.DateTimeField()
    reason_for_visit = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    created_at= models.DateTimeField(auto_now_add=True)
    history= HistoricalRecords()

    def __str__(self):
        return f"Appointment: {self.patient.user.last_name} with Dr. {self.doctor.user.last_name} on {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"
    

class Vitals(models.Model):
    patient=models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='vitals')
    recorded_at=models.DateTimeField(auto_now_add=True)
    temperature=models.DecimalField(max_digits=4, decimal_places=1, help_text="in Celsius")
    blood_pressure=models.CharField(max_length=10, help_text="e.g., 120/80")
    respiratory_rate=models.PositiveIntegerField(blank=True, null=True)
    appointment=models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='vitals')
    pulse_rate=models.IntegerField(help_text="beats per minute")
    weight=models.DecimalField(max_digits=5, decimal_places=2, help_text="in kg")
    recorded_by=models.ForeignKey(NurseProfile, on_delete=models.SET_NULL, null=True)
    recorded_at=models.DateTimeField(auto_now_add=True)
    history=HistoricalRecords()

    def __str__(self):
        return f"Vitals for {self.appointment.patient.user.first_name}"
    

class Consultation(models.Model):
    patient=models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='consultations')
    appointment=models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='consultation')
    doctor=models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='consultations')
    vitals=models.OneToOneField(Vitals, on_delete=models.SET_NULL, null=True, blank=True)
    symptoms=models.TextField(help_text="Chief complaints reported by the patient")
    diagnosis=models.TextField()
    plan=models.TextField(help_text="Treatment Plan")
    is_follow_up=models.BooleanField(default=False)
    notes=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    history=HistoricalRecords()

    def __str__(self):
        return f"Consultation for {self.appointment.patient.user.last_name} by Dr. {self.doctor.user.last_name}"
    
class Prescription(models.Model):
    consultation=models.OneToOneField(Consultation, on_delete=models.CASCADE, related_name='prescription')
    doctor=models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient=models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    date_prescribed=models.DateTimeField(auto_now_add=True)
    notes=models.TextField(blank=True, null=True)
    is_dispensed=models.BooleanField(default=False)
    dispensed_by=models.ForeignKey(PharmacistProfile, on_delete=models.SET_NULL, null=True, blank=True)
    history=HistoricalRecords()
    

    def __str__(self):
        return f"Prescription for {self.patient.user.last_name} ({self.date_prescribed.date()})"
    
class PrescriptionItem(models.Model):
    prescription=models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medicine_name=models.CharField(max_length=200)
    dosage=models.CharField(max_length=100, help_text="e.g., 500mg")
    frequency=models.CharField(max_length=100, help_text="e.g., 3 times a day")
    duration=models.CharField(max_length=100, help_text="e.g., 7 days")

    def __str__(self):
        return f"{self.medicine_name} - {self.dosage}"
    
class LabRequest(models.Model):
    PRIORITY_CHOICES=(('ROUTINE', 'Routine'), ('URGENT', 'Urgent'))
    STATUS_CHOICES=(
        ('REQUESTED','Requested'),
        ('COLLECTED', 'Sample Collected'),
        ('PENDING', 'Pending Results'),
        ('COMPLETED', 'Completed'),
    )
    consultation=models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='lab_requests')
    doctor=models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient=models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    lab_tech=models.ForeignKey(LabTechProfile, on_delete=models.SET_NULL, null=True, blank=True)
    test_name=models.CharField(max_length=255)
    priority=models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='ROUTINE')
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    result_notes=models.TextField(blank=True, null=True)
    result_file=models.FileField(upload_to='lab_results/', blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    completed_at=models.DateTimeField(null=True, blank=True)
    history=HistoricalRecords()

    def __str__(self):
        return f"{self.test_name} for {self.patient.user.last_name}"
