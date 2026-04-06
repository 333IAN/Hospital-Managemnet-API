from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LabRequest
from billing.models import Invoice, InvoiceItem

@receiver(post_save, sender=LabRequest)
def bill_lab_test(sender, instance, created, **kwargs):
    if instance.status=='COMPLETED':
        invoice,_=Invoice.objects.get_or_create(
            patient=instance.patient,
            status='PENDING'
        )

        exists=InvoiceItem.objects.filter(
            invoice=invoice,
            item_name=f"Lab: {instance.test_type.name}"
        ).exists()

        if not exists:
            InvoiceItem.objects.create(
                invoice=invoice,
                item_name=f"Lab: {instance.test_type.name}",
                quantity=1,
                unit_price=instance.test_type.base_price
            )