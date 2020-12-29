from django.forms import ModelForm, TextInput
from .models import City


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widget = {"name": TextInput(attrs={'class':"input-field", 'placeholder':'add city'})}