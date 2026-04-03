from rest_framework import serializers
from .models import Group
from users.models import User

# --- Базовый юзер (для отображения) ---
class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


# --- ДЛЯ АДМИНА (CRUD) ---
class GroupAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'teacher', 'students', 'day_of_week', 'start_time']

    def validate_teacher(self, value):
        if value and value.role != 'teacher':
            raise serializers.ValidationError("User must be a teacher")
        return value

    def validate_students(self, value):
        if not value:
            return value
        for user in value:
            if user.role != 'student':
                raise serializers.ValidationError("All must be students")
        return value


# --- ДЛЯ УЧИТЕЛЯ (read only, с именами) ---
class GroupTeacherSerializer(serializers.ModelSerializer):
    teacher = UserSimpleSerializer(read_only=True)
    students = UserSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'teacher', 'students', 'day_of_week', 'start_time']


# --- ДЛЯ УЧЕНИКА (тоже read only) ---
class GroupStudentSerializer(serializers.ModelSerializer):
    teacher = UserSimpleSerializer(read_only=True)
    students = UserSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'teacher', 'students', 'day_of_week', 'start_time']