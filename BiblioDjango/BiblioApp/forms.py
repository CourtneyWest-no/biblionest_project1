from django import forms
from .models import Reference

class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = ['title', 'author', 'publication_date', 'source']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }