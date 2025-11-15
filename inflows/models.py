from django.db import models
from geladinhos.models import Geladinho


class Inflow(models.Model):
    geladinho = models.ForeignKey(
        Geladinho,
        on_delete=models.PROTECT,
        related_name='inflows',
    )
    quantity = models.IntegerField(
        verbose_name='Quantidade',
    )
    manufacturing_date = models.DateTimeField(
        verbose_name='Data de Fabricacao',
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name='descrição'
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
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

    def __str__(self):
        return str(self.geladinho)