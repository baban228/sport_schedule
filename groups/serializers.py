from rest_framework import serializers
from .models import Group
from users.models import User

# базовый юзер
class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


# админ
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


# учитель
class GroupTeacherSerializer(serializers.ModelSerializer):
    teacher = UserSimpleSerializer(read_only=True)
    students = UserSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'teacher', 'students', 'day_of_week', 'start_time']


# ученик
class GroupStudentSerializer(serializers.ModelSerializer):
    teacher = serializers.CharField(source='teacher.username', read_only=True)
    students = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Group
        # все нужные поля
        fields = [
            'id',
            'name',
            'teacher',
            'students',
            'color',
            'day_of_week',
            'start_time'
        ]