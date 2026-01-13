from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    preview = models.ImageField(
        upload_to="course_previews/", blank=True, null=True, verbose_name="Превью"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    owner = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        related_name="courses",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    preview = models.ImageField(
        upload_to="lesson_previews/", blank=True, null=True, verbose_name="Превью"
    )
    video_url = models.URLField(
        max_length=500, blank=True, null=True, verbose_name="Ссылка на видео"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )
    owner = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        related_name="lessons",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    user = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, related_name="subscriptions"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="subscriptions"
    )

    class Meta:
        unique_together = ("user", "course")
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user.email} → {self.course.title}"
