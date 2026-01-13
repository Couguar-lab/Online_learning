from rest_framework import serializers

from .models import Course, Lesson, Subscription
from .validators import YouTubeURLValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор урока."""

    video_url = serializers.URLField(
        required=False,
        allow_blank=True,
        allow_null=True,
        validators=[YouTubeURLValidator(field="video_url")],
    )

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "description",
            "preview",
            "video_url",
            "course",
            "owner",
        )


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курса с количеством уроков, списком уроков и признаком подписки."""

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "preview",
            "description",
            "lessons_count",
            "lessons",
            "is_subscribed",
            "owner",
        )

    def get_lessons_count(self, obj):
        """Количество уроков в курсе."""
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Признак подписки текущего пользователя."""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False
