from django.db import models
from rest_framework.exceptions import ValidationError

from groups.models import Group

class Lesson(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    title = models.CharField(max_length=255)

    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

def clean(self):
    overlapping = Lesson.objects.filter(
        group=self.group,
        start_time__lt=self.end_time,
        end_time__gt=self.start_time
    )

    if overlapping.exists():
        raise ValidationError("Time conflict")