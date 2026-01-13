from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from lms.models import Course, Lesson

User = get_user_model()


class LessonCRUDTests(APITestCase):
    """Тесты CRUD операций с уроками с учётом прав доступа."""

    def setUp(self):
        # Обычный пользователь
        self.user = User.objects.create_user(email="user@test.com", password="pass123")
        # Модератор
        self.moderator = User.objects.create_user(
            email="mod@test.com", password="pass123"
        )
        self.moderator.groups.create(name="moderators")

        # Курс и урок, принадлежащие обычному пользователю
        self.course = Course.objects.create(title="Test Course", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            course=self.course,
            owner=self.user,
            video_url="https://youtube.com/watch?v=test",
        )

        self.client = APIClient()

    def test_create_lesson_as_owner(self):
        """Обычный пользователь может создать урок."""
        self.client.force_authenticate(self.user)
        url = reverse("lms:lesson-list")
        data = {
            "title": "New Lesson",
            "course": self.course.id,
            "video_url": "https://youtube.com/watch?v=new",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_as_moderator_forbidden(self):
        """Модератор не может создавать уроки."""
        self.client.force_authenticate(self.moderator)
        url = reverse("lms:lesson-list")
        data = {"title": "Forbidden Lesson", "course": self.course.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_own_lesson(self):
        """Владелец может редактировать свой урок."""
        self.client.force_authenticate(self.user)
        url = reverse("lms:lesson-detail", kwargs={"pk": self.lesson.pk})
        data = {"title": "Updated Lesson"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_update_lesson_as_moderator(self):
        """Модератор может редактировать любой урок."""
        self.client.force_authenticate(self.moderator)
        url = reverse("lms:lesson-detail", kwargs={"pk": self.lesson.pk})
        data = {"title": "Moderated Update"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_youtube_link(self):
        """Запрещена ссылка не на YouTube."""
        self.client.force_authenticate(self.user)
        url = reverse("lms:lesson-list")
        data = {
            "title": "Bad Link",
            "course": self.course.id,
            "video_url": "https://vimeo.com/123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Разрешены только ссылки на YouTube", str(response.data))
