from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import QuotationItem

@receiver([post_save, post_delete], sender=QuotationItem)
def update_quotation_total(sender, instance, **kwargs):
    instance.quotation.update_total_amount()