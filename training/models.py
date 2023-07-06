from django.db import models
from exercises.models import Exercises
from django.core.exceptions import ValidationError
from app import settings


class Training(models.Model):
    SETS = 'Sets'
    TIME = 'Time'

    TYPE_CHOICES = [
        (SETS, 'Sets'),
        (TIME, 'Time'),
    ]

    exercise = models.ForeignKey(Exercises, on_delete=models.CASCADE)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default=SETS)
    quantity = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Exercise {self.exercise.name} by {self.username.username}"

    def save(self, *args, **kwargs):
        if self.exercise.username != self.username:
            raise ValidationError("You can only use your own exercises.")
        super().save(*args, **kwargs)
