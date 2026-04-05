from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    MealViewSet,
    MealItemViewSet,
    NutritionStatsViewSet
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'meals', MealViewSet, basename='meals')
router.register(r'meal-items', MealItemViewSet, basename='meal-items')
router.register(r'nutrition-stats', NutritionStatsViewSet, basename='nutrition-stats')

urlpatterns = router.urls