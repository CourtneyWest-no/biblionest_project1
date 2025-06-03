from django import forms
from .models import Reference, Tag
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class ReferenceForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    new_tags = forms.CharField(
        max_length=255,
        required=False,
        help_text="Enter new tags separated by commas."
    )
    title = forms.CharField(required=True)
    author = forms.CharField(required=True)
    publication_date = forms.DateField(required=True)
    source = forms.CharField(required=True)

    class Meta:
        model = Reference
        fields = ['title', 'author', 'publication_date', 'source', 'tags', 'new_tags']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']