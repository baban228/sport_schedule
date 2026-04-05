from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL


class Product(models.Model):
    name = models.CharField(max_length=255)

    calories = models.FloatField(help_text="Ккал на 100г")
    protein = models.FloatField(help_text="Белки на 100г")
    fat = models.FloatField(help_text="Жиры на 100г")
    carbs = models.FloatField(help_text="Углеводы на 100г")

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_products'
    )

    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Meal(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'),
        ('snack', 'Перекус'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='meals'
    )

    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Проверка: только ученик
        if self.user.role != 'student':
            raise ValidationError("Только ученики могут вести дневник питания")

    def __str__(self):
        return f"{self.user} - {self.meal_type} ({self.date})"

    @property
    def total_calories(self):
        return sum(item.total_calories for item in self.items.all())

    @property
    def total_protein(self):
        return sum(item.total_protein for item in self.items.all())

    @property
    def total_fat(self):
        return sum(item.total_fat for item in self.items.all())

    @property
    def total_carbs(self):
        return sum(item.total_carbs for item in self.items.all())


class MealItem(models.Model):
    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='meal_items'
    )

    weight = models.FloatField(help_text="Вес в граммах")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} ({self.weight}г)"

    @property
    def total_calories(self):
        return (self.product.calories * self.weight) / 100

    @property
    def total_protein(self):
        return (self.product.protein * self.weight) / 100

    @property
    def total_fat(self):
        return (self.product.fat * self.weight) / 100

    @property
    def total_carbs(self):
        return (self.product.carbs * self.weight) / 100


class DailyGoal(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='daily_goal'
    )

    calories = models.FloatField(default=2000)
    protein = models.FloatField(default=150)
    fat = models.FloatField(default=70)
    carbs = models.FloatField(default=250)

    def clean(self):
        if self.user.role != 'student':
            raise ValidationError("Цели доступны только ученикам")

    def __str__(self):
        return f"Цель {self.user}"