from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Message, Advert, Application, Review, Subject, Material


class AdvertForm(ModelForm):
    class Meta:
        model = Advert
        fields = '__all__'