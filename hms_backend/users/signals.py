from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, PatientProfile, DoctorProfile, NurseProfile, PharmacistProfile, LabTechProfile, RadiologistProfile, ReceptionistProfile
import datetime


def generate_hms_id(prefix, model_class, id_field):
    current_year = datetime.datetime.now().year
    last_instance = model_class.objects.order_by('id').last()

    if not last_instance or not getattr(last_instance, id_field):
        new_number = 1
    else:
        last_id_str=getattr(last_instance, id_field)
        try:
            last_number=int(last_id_str.split('-')[-1])
            new_number=last_number+1
        except (IndexError, ValueError):
            new_number=1

    return f"{prefix}-{current_year}-{new_number:04d}"


@receiver(post_save, sender=User)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role=='PATIENT':
            new_id=generate_hms_id('PAT', PatientProfile, 'patient_id')
            PatientProfile.objects.create(user=instance, patient_id=new_id)
        elif instance.role=='DOCTOR':
            new_id=generate_hms_id('DOC', DoctorProfile, 'employee_id')
            DoctorProfile.objects.create(user=instance, employee_id=new_id)
        elif instance.role=='NURSE':
            new_id=generate_hms_id('NUR', NurseProfile, 'employee_id')
            NurseProfile.objects.create(user=instance, employee_id=new_id)
        elif instance.role=='PHARMACIST':
            new_id=generate_hms_id('PHA', PharmacistProfile, 'employee_id')
            PharmacistProfile.objects.create(user=instance, employee_id=new_id)
        elif instance.role=='LAB_TECH':
            new_id=generate_hms_id('LAB', LabTechProfile, 'employee_id')
            LabTechProfile.objects.create(user=instance, employee_id=new_id)
        elif instance.role=='RADIOLOGIST':
            new_id=generate_hms_id('RAD', RadiologistProfile, 'employee_id')
            RadiologistProfile.objects.create(user=instance, employee_id=new_id)
        elif instance.role=='RECEPTIONIST':
            new_id=generate_hms_id('REC', ReceptionistProfile, 'employee_id')
            ReceptionistProfile.objects.create(user=instance, employee_id=new_id)

@receiver(post_save, sender=User)

def save_user_profile(sender, instance, **kwargs):
    try:
        if instance.role=='PATIENT':
            instance.patient_profile.save()
        elif instance.role=='DOCTOR':
            instance.doctor_profile.save()
        elif instance.role=='NURSE':
            instance.nurse_profile.save()
        elif instance.role=='PHARMACIST':
            instance.pharmacist_profile.save()
        elif instance.role=='LAB_TECH':
            instance.labtech_profile.save()
        elif instance.role=='RADIOLOGIST':
            instance.radiologist_profile.save()
        elif instance.role=='RECEPTIONIST':
            instance.receptionist_profile.save()
    except AttributeError:
        pass