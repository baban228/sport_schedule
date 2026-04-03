from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
# ViewSet'ы
from groups.views import (
    GroupAdminViewSet,
    TeacherGroupViewSet,
    StudentGroupViewSet
)

# страницы (твои HTML)
from config.views import home, admin_dashboard, teacher_dashboard, student_dashboard, register_view

# JWT (если используешь)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# --- DRF Router ---
router = DefaultRouter()

# Админ управляет группами
router.register(r'groups', GroupAdminViewSet, basename='groups')

# Учитель видит свои группы
router.register(r'teacher-groups', TeacherGroupViewSet, basename='teacher-groups')

# Ученик видит свои группы
router.register(r'student-groups', StudentGroupViewSet, basename='student-groups')


urlpatterns = [
    # Главная
    path('', home, name='home'),

    # Дашборды
    path('admin-panel/', admin_dashboard, name='admin-dashboard'),
    path('teacher/', teacher_dashboard, name='teacher-dashboard'),
    path('student/', student_dashboard, name='student-dashboard'),


    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", register_view, name="register"),  # регистрация
    # Django admin (встроенный)
    path('django-admin/', admin.site.urls),

    # API
    path('api/', include(router.urls)),

    # JWT (если используешь)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

