from django import forms
from .models import Inflow


class InflowForm(forms.ModelForm):
    class Meta:
        model = Inflow
        fields = ['geladinho', 'quantity', 'manufacturing_date', 'description']
        widgets = {
            'geladinho': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'quantity': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'manufacturing_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }
        labels = {
            'geladinho': 'Geladinho',
            'quantity': 'Quantidade',
            'manufacturing_date': 'Data de Fabricação',
            'description': 'Descrição',
        }
