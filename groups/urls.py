from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherGroupViewSet

router = DefaultRouter()
router.register(r'teacher-groups', TeacherGroupViewSet, basename='teacher-groups')

urlpatterns = [
    path('api/', include(router.urls)),
]