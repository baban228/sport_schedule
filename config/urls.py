from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView 

from groups.views import (
    GroupAdminViewSet,
    TeacherGroupViewSet,
    StudentGroupViewSet
)

from config.views import home, admin_dashboard, teacher_dashboard, student_dashboard, register_view, diet_dashboard, login_view


# router для групп
router = DefaultRouter()

router.register(r'groups', GroupAdminViewSet, basename='groups')
router.register(r'teacher-groups', TeacherGroupViewSet, basename='teacher-groups')
router.register(r'student-groups', StudentGroupViewSet, basename='student-groups')


urlpatterns = [
    # Главная
    path('', home, name='home'),

    # Дашборды
    path('admin-panel/', admin_dashboard, name='admin-dashboard'),
    path('teacher/', teacher_dashboard, name='teacher-dashboard'),
    path('student/', student_dashboard, name='student-dashboard'),

    # auth
    path("login/", login_view, name="login"),  # ← ИЗМЕНЕНО
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", register_view, name="register"),

    # admin
    path('django-admin/', admin.site.urls),

    path('diet/', diet_dashboard, name='diet'),

    # API
    path('api/', include(router.urls)),

    path('api/nutrition/', include('nutrition.urls')),
]