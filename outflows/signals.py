import logging

from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from outflows.models import Outflow
from services.notify import Notify


logger = logging.getLogger(__name__)
notify = Notify()


@receiver(post_save, sender=Outflow)
def update_geladinho_quantity(sender, instance, created, **kwargs):
    if created:
        if instance.quantity > 0:
            geladinho = instance.geladinho
            if instance.quantity <= geladinho.quantity:
                geladinho.quantity -= instance.quantity
                geladinho.save()


@receiver(post_save, sender=Outflow)
def send_outflow_event(sender, instance, created, **kwargs):
    if created:
        try:
            data = dict(
                event_type='create_outflow',
                outflow=instance.id,
                geladinho=instance.geladinho.flavor,
                geladinho_id=instance.geladinho.id,
                quantity=instance.quantity,
                timestamp_created_at=timezone.localtime(
                    instance.created_at
                ).strftime("%Y/%m/%d, %H:%M:%S"),
                selling_price=float(
                    instance.geladinho.selling_price
                    if instance.selling_price_outflow is None
                    else instance.selling_price_outflow
                ),
                description=instance.description,
            )

            notify.send_outflow_event(data)

        except Exception as e:
            logger.error(f"[ERRO SIGNAL Outflow] {e}")
            pass
