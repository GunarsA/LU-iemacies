from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100, blank=True)

    def chats(self):
        return Message.objects.filter(sender=self.user) | Message.objects.filter(receiver=self.user)


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sender'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receiver'
    )
    message = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Advert(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(
        'Subject',
        on_delete=models.CASCADE,
        related_name='adverts'
    )
    description = models.TextField(blank=True)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING'
        ONGOING = 'ONGOING'
        FINISHED = 'FINISHED'

    advert = models.ForeignKey(
        Advert,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    description = models.CharField(max_length=1000)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    advert = models.ForeignKey(
        Advert,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    review = models.CharField(max_length=1000, blank=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Complaint(models.Model):
    advert = models.ForeignKey(
        Advert,
        on_delete=models.CASCADE,
        related_name='complaints'
    )
    complainant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='complaints'
    )
    description = models.CharField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Subject(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    sub_subjects = models.ManyToManyField(
        'Subject',
        blank=True,
        related_name='sup_subjects'
    )
    pursuers = models.ManyToManyField(
        User,
        blank=True,
        related_name='goals'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class Material(models.Model):
    subjects = models.ManyToManyField(Subject, related_name='materials')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    completers = models.ManyToManyField(
        User,
        blank=True,
        related_name='completions'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
