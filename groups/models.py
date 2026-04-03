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

    # Новые поля
    DAY_CHOICES = [
        ('Mon', 'Понедельник'),
        ('Tue', 'Вторник'),
        ('Wed', 'Среда'),
        ('Thu', 'Четверг'),
        ('Fri', 'Пятница'),
        ('Sat', 'Суббота'),
        ('Sun', 'Воскресенье'),
    ]
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES, default='Mon')
    start_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.day_of_week} {self.start_time})"