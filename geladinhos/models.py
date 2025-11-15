from django.db import models


class Geladinho(models.Model):
    flavor = models.CharField(
        max_length=100,
        verbose_name='Sabor',
    )
    quantity = models.IntegerField(
        default=0,
        verbose_name='Quantidade',
    )
    description = models.CharField(
        verbose_name='Descrição',
    )
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Preço de custo',
    )
    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Preço de Venda',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em',
    )

    class Meta:
        ordering = ['-quantity']

    def __str__(self):
        return self.flavor
