from rest_framework import serializers
from .models import Product, Meal, MealItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class MealItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_calories = serializers.FloatField(read_only=True)
    total_protein = serializers.FloatField(read_only=True)
    total_fat = serializers.FloatField(read_only=True)
    total_carbs = serializers.FloatField(read_only=True)

    class Meta:
        model = MealItem
        fields = [
            'id',
            'product',
            'product_name',
            'weight',
            'total_calories',
            'total_protein',
            'total_fat',
            'total_carbs'
        ]


class MealSerializer(serializers.ModelSerializer):
    items = MealItemSerializer(many=True, read_only=True)
    total_calories = serializers.FloatField(read_only=True)
    total_protein = serializers.FloatField(read_only=True)
    total_fat = serializers.FloatField(read_only=True)
    total_carbs = serializers.FloatField(read_only=True)

    class Meta:
        model = Meal
        fields = [
            'id',
            'meal_type',
            'date',
            'items',
            'total_calories',
            'total_protein',
            'total_fat',
            'total_carbs'
        ]