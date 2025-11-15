from django.db import models
from geladinhos.models import Geladinho


class Outflow(models.Model):
    geladinho = models.ForeignKey(
        Geladinho,
        on_delete=models.PROTECT,
        related_name='outflows',
    )
    quantity = models.IntegerField(
        verbose_name='Quantidade',
    )
    description = models.TextField(
        verbose_name='descrição'
    )
    selling_price_outflow = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Preço de Venda de Saída',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Saída'
        verbose_name_plural = 'Saídas'

    def __str__(self):
        return str(self.geladinho)
