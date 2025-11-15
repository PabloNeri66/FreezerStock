from django import forms
from django.core.exceptions import ValidationError
from .models import Outflow


class OutflowForm(forms.ModelForm):
    class Meta:
        model = Outflow
        fields = [
            'geladinho', 'quantity', 'description', 'selling_price_outflow',
        ]
        widgets = {
            'supplier': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'geladinho': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'quantity': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'selling_price_outflow': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
        }

        labels = {
            'geladinho': 'Produto',
            'quantity': 'Quantidade',
            'description': 'Descrição',
            'selling_price_outflow': 'Preco de venda de saída',
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        geladinho = self.cleaned_data.get('geladinho')

        if quantity > geladinho.quantity:
            raise ValidationError(
                f'A quantidade disponível em estoque para o geladinho {geladinho.flavor} é de {geladinho.quantity}'
            )
        return quantity