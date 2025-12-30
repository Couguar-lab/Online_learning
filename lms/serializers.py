from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор урока."""
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'description', 'preview', 'video_url', 'course')


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курса с количеством и списком уроков."""
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'preview', 'description', 'lessons_count', 'lessons')

    def get_lessons_count(self, obj):
        """Количество уроков в курсе."""
        return obj.lessons.count()