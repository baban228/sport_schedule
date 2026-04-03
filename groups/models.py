from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Group(models.Model):
    name = models.CharField(max_length=255)

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='teaching_groups'
    )

    students = models.ManyToManyField(
        User,
        related_name='student_groups'
    )

    color = models.CharField(max_length=7, default='#FFFFFF')

    def __str__(self):
        return self.name