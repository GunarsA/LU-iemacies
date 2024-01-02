from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100, blank=True)

    description = models.TextField(blank=True)

    def reachable_users(self):
        """
        Returns a queryset of users who are reachable by the current user.
        Reachable users include teachers, students, and users with whom the current user has existing chats.
        """
        teachers = set(Application.objects.filter(
            applicant=self.user).values_list('advert__owner', flat=True))
        students = set(Application.objects.filter(
            advert__owner=self.user).values_list('applicant', flat=True))
        existing_chats = set(Chat.objects.filter(sender=self.user).values_list('receiver', flat=True)) | set(
            Chat.objects.filter(receiver=self.user).values_list('sender', flat=True))
        return User.objects.filter(id__in=teachers | students | existing_chats).exclude(id=self.user.id)

    def __str__(self) -> str:
        return self.user.username


class Chat(models.Model):
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

    def __str__(self) -> str:
        return f'{self.sender} -> {self.receiver}'


class Advert(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(
        'Subject',
        on_delete=models.CASCADE,
        related_name='adverts'
    )
    description = models.TextField(blank=True)
    price = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['owner', 'subject']]

    def get_average_rating(self):
        return self.reviews.aggregate(models.Avg('rating'))['rating__avg']

    def __str__(self) -> str:
        return f'{self.owner} - {self.subject}'


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

    class Meta:
        unique_together = [['advert', 'applicant']]

    def __str__(self) -> str:
        return f'{self.applicant} - {self.advert}'


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

    class Meta:
        unique_together = [['advert', 'reviewer']]

    def __str__(self) -> str:
        return f'{self.reviewer} - {self.advert}'


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
