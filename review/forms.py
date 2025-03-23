
from django.forms import ModelForm
from .models import menu


class add_menu(ModelForm):
    class Meta:
        model = menu
        fields = '__all__'