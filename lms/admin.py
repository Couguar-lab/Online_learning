from django.contrib import admin
from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Админка для курсов."""
    list_display = ('title', 'description')
    search_fields = ('title',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Админка для уроков."""
    list_display = ('title', 'course')
    list_filter = ('course',)
    search_fields = ('title',)