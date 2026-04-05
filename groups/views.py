from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Group
from .serializers import (
    GroupAdminSerializer,
    GroupTeacherSerializer,
    GroupStudentSerializer
)
from .permissions import IsAdminOrReadOnly


# админ
class GroupAdminViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        return Group.objects.all()

    def perform_create(self, serializer):
        if self.request.user.role != 'admin':
            raise PermissionDenied("Только админ может создавать группы")
        serializer.save()


# учитель
class TeacherGroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GroupTeacherSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != 'teacher':
            return Group.objects.none()
        return Group.objects.filter(teacher=user)


# ученик
class StudentGroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GroupStudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != 'student':
            return Group.objects.none()
        return Group.objects.filter(students=user)