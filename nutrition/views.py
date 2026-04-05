from datetime import timedelta
from django.utils.timezone import now

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Product, Meal, MealItem
from .serializers import ProductSerializer, MealSerializer, MealItemSerializer


# 🔹 Продукты
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Product.objects.all()
        search = self.request.query_params.get('search')

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset


# 🔹 Приемы пищи
class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # 📅 Дневник за сегодня
    @action(detail=False, methods=['get'])
    def today(self, request):
        today = now().date()
        meals = self.get_queryset().filter(date=today)

        serializer = self.get_serializer(meals, many=True)
        return Response(serializer.data)


# 🔹 Элементы еды
class MealItemViewSet(viewsets.ModelViewSet):
    serializer_class = MealItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MealItem.objects.filter(meal__user=self.request.user)


# 📊 Статистика
class NutritionStatsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    # 🔥 Сегодня
    @action(detail=False, methods=['get'])
    def today(self, request):
        user = request.user
        today = now().date()

        meals = Meal.objects.filter(user=user, date=today)
        return Response(self.calculate_totals(meals))

    # 🔥 Неделя (для графика)
    @action(detail=False, methods=['get'])
    def week(self, request):
        user = request.user
        today = now().date()

        data = []

        for i in range(7):
            day = today - timedelta(days=i)
            meals = Meal.objects.filter(user=user, date=day)

            totals = self.calculate_totals(meals)

            data.append({
                "date": day,
                **totals
            })

        return Response(list(reversed(data)))

    # 🧠 Подсчет
    def calculate_totals(self, meals):
        calories = protein = fat = carbs = 0

        for meal in meals:
            for item in meal.items.all():
                calories += item.total_calories
                protein += item.total_protein
                fat += item.total_fat
                carbs += item.total_carbs

        return {
            "calories": round(calories, 2),
            "protein": round(protein, 2),
            "fat": round(fat, 2),
            "carbs": round(carbs, 2),
        }