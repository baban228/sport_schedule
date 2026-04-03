from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Lesson

class MyScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == 'teacher':
            lessons = Lesson.objects.filter(group__teacher=user)
        else:
            lessons = Lesson.objects.filter(group__students=user)

        data = [
            {
                "id": lesson.id,
                "title": lesson.title,
                "start_time": lesson.start_time,
                "end_time": lesson.end_time,
                "group": lesson.group.name,
                "color": lesson.group.color,
            }
            for lesson in lessons
        ]

        return Response(data)