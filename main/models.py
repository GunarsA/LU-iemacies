from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Profile(models.Model):
    full_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def reachable_users(self) -> models.QuerySet[User]:
        """
        Returns a queryset of users who are reachable by the current user.

        The reachable users include both the teachers who have ongoing applications
        from the current user and the students who have ongoing applications to the
        advertisements owned by the current user.

        Returns:
            A queryset of User objects representing the reachable users.
        """
        teachers = set(Application.objects.filter(
            applicant=self.user, status='ONGOING').values_list('advert__owner', flat=True))
        students = set(Application.objects.filter(
            advert__owner=self.user, status='ONGOING').values_list('applicant', flat=True))
        return User.objects.filter(id__in=teachers | students | {self.user.id})

    def viewable_users(self) -> models.QuerySet[User]:
        """
        Returns a queryset of users that can be viewed by the current user.

        This method retrieves the set of reachable users and existing chats
        involving the current user. It then filters the User queryset based on
        the union of these sets.

        Returns:
            A queryset of User objects that can be viewed by the current user.
        """
        application_relations = set(
            self.reachable_users().values_list('id', flat=True))
        existing_chats = set(Chat.objects.filter(sender=self.user).values_list('receiver', flat=True)) | set(
            Chat.objects.filter(receiver=self.user).values_list('sender', flat=True))
        return User.objects.filter(id__in=application_relations | existing_chats)

    def __str__(self) -> str:
        return self.user.username


class Chat(models.Model):
    message = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    def __str__(self) -> str:
        return f'{self.sender} -> {self.receiver}'


class Advert(models.Model):
    description = models.TextField(blank=True)
    price = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='adverts'
    )
    subject = models.ForeignKey(
        'Subject',
        on_delete=models.CASCADE,
        related_name='adverts'
    )

    def get_average_rating(self) -> float:
        """
        Calculates and returns the average rating of the reviews for this object.

        Returns:
            float: The average rating.
        """
        return self.reviews.aggregate(models.Avg('rating'))['rating__avg']

    def __str__(self) -> str:
        return f'{self.owner} - {self.subject}'

    class Meta:
        unique_together = [['owner', 'subject']]


class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING'
        ONGOING = 'ONGOING'
        FINISHED = 'FINISHED'
        REJECTED = 'REJECTED'

    description = models.CharField(max_length=1000)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    class Meta:
        unique_together = [['advert', 'applicant']]

    def __str__(self) -> str:
        return f'{self.applicant} - {self.advert}'


class Review(models.Model):
    review = models.CharField(max_length=1000, blank=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    class Meta:
        unique_together = [['advert', 'reviewer']]

    def __str__(self) -> str:
        return f'{self.reviewer} - {self.advert}'


class Subject(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    sub_subjects = models.ManyToManyField(
        'Subject',
        blank=True,
        related_name='sup_subjects'
    )

    def __str__(self):
        return self.title
