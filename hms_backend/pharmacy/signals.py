from django.db.models.signals import post_save
import logging
from django.dispatch import receiver
from django.db import transaction
from .models import Prescription, Stock
from billing.models import Invoice, InvoiceItem

logger=logging.getLogger(__name__)

@receiver(post_save, sender=Prescription)
def process_dispensing(sender, instance, created, **kwargs):
    if instance.status=='DISPENSED':
        with transaction.atomic():
            available_stocks=Stock.objects.filter(medication=instance.medication, quantity_in_stock__gt=0).order_by('expiry_date')
            if not available_stocks.exists():
                raise ValueError(f"No stock available for {instance.medication.name}")
            target_stock=available_stocks.first()
            target_stock.quantity_in_stock-=1
            target_stock.save()

            invoice, _=Invoice.objects.get_or_create(
                patient=instance.patient, 
                status='PENDING',
            )
            InvoiceItem.objects.create(
                invoice=invoice,
                item_name=f"Dispensed: {instance.medication.name} ({instance.medication.strength})",
                quantity=1,
                unit_price=instance.medication.unit_price
            )
@receiver(post_save, sender=Stock)
def check_stock_levels(sender, instance, **kwargs):
    if instance.quantity_in_stock<+instance.reorder_level:
        alert_msg=(
            f"INVENTORY ALERT: {instance.medication.name} (Batch: {instance.batch_number}) "
            f"is low. Current: {instance.quantity_in_stock}, Level: {instance.reorder_level}"
        )
        print(alert_msg)
        logger.warning(alert_msg)


