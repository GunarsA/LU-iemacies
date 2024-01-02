from django.forms import ModelForm
from .models import Advert, Application, Review


class AdvertForm(ModelForm):
    class Meta:
        model = Advert
        fields = '__all__'
        exclude = ['owner']


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['description']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review']
