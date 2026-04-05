from django.contrib import admin
from .models import Group
from schedule.models import Lesson

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1  # количество пустых форм для добавления сразу

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')
    list_filter = ('teacher',)
    search_fields = ('name',)
    filter_horizontal = ('students',)
    inlines = [LessonInline]