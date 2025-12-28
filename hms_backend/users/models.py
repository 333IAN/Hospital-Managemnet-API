from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from simple_history.models import HistoricalRecords
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('DOCTOR', 'Doctor'),
        ('NURSE', 'Nurse'),
        ('PHARMACIST', 'Pharmacist'),
        ('RECEPTIONIST', 'Receptionist'),
        ('LAB_TECH', 'Lab Technician'),
        ('RADIOLOGIST', 'Radiologist'),
        ('PATIENT', 'Patient'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        return f"{self.email} ({self.role})"
    

class BaseStaffProfile(models.Model):
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    history= HistoricalRecords(inherit=True)


    class Meta:
        abstract = True 

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    patient_id=models.CharField(max_length=20, unique=True, null=True, blank=True)
    date_of_birth = models.DateField()
    blood_group=models.CharField(max_length=5)
    emergency_contact = models.CharField(max_length=100)
    history= HistoricalRecords()


class DoctorProfile(BaseStaffProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100)
    is_on_call = models.BooleanField(default=False)

class NurseProfile(BaseStaffProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nurse_profile')
    ward=models.CharField(max_length=100)

class PharmacistProfile(BaseStaffProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pharmacist_profile')
    is_inventory_manager = models.BooleanField(default=False)

class LabTechProfile(BaseStaffProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lab_tech_profile')
    lab_certification= models.CharField(max_length=100)

class RadiologistProfile(BaseStaffProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='radiologist_profile')
    modality= models.CharField(max_length=100)

class ReceptionistProfile(BaseStaffProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='receptionist_profile')
    department= models.CharField(max_length=100, default='Front Desk')