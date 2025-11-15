from django import forms
from .models import Geladinho


class GeladinhoForm(forms.ModelForm):
    class Meta:
        model = Geladinho
        fields = [
            'flavor', 'description', 'cost_price', 'selling_price',
        ]
        widgets = {
            'flavor': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'flavor': 'Sabor',
            'description': 'Descrição',
            'cost_price': 'Preço de Custo',
            'selling_price': 'Preço de Venda',
        }
