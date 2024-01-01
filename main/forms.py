from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Advert, Application


class AdvertForm(ModelForm):
    class Meta:
        model = Advert
        fields = '__all__'
        exclude = ['owner']


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['description']
