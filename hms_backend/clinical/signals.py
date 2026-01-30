from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Consultation
from billing.models import Invoice, InvoiceItem

@receiver(post_save, sender=Consultation)
def auto_bill_consultation_fee(sender, instance, created, **kwargs):
    if created:
        CONSULTATION_FEE=500.00
        with transaction.atomic():
            invoice, _=Invoice.objects.get_or_created(
                patient=instance.patient,
                status='PENDING',
                defaults={'total_amount': 0}
            )

            InvoiceItem.objects.create(
                invoice=invoice,
                item_name=f"Consultation Fee - Dr. {instance.doctor.user.last_name}",
                quantity=1,
                unit_price=CONSULTATION_FEE
            )
            