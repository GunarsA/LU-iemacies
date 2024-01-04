from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from .models import Profile, Advert, Application, Review


class UserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'description']


class AdvertForm(ModelForm):
    class Meta:
        model = Advert
        fields = ['subject', 'description', 'price', 'is_active']


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['description']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review']
