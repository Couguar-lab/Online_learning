from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserTests(APITestCase):
    """Тесты для эндпоинтов пользователей и профиля."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            password="pass123",
            phone="+79991234567",
            city="Moscow",
        )
        self.other_user = User.objects.create_user(
            email="other@test.com", password="pass123"
        )
        self.moderator = User.objects.create_user(
            email="mod@test.com", password="pass123"
        )
        self.moderator.groups.create(name="moderators")

    def test_get_own_profile(self):
        """Авторизованный пользователь видит свой полный профиль."""
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse("users:user-detail", kwargs={"pk": self.user.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("phone", response.data)
        self.assertIn("city", response.data)
        self.assertIn("payments", response.data)  # история платежей

    def test_get_other_profile(self):
        """Просмотр чужого профиля — без чувствительных данных."""
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse("users:user-detail", kwargs={"pk": self.other_user.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("payments", response.data)  # нет платежей
        self.assertIn("phone", response.data)  # phone и city видны (общая информация)
        self.assertIn("city", response.data)

    def test_update_own_profile(self):
        """Пользователь может редактировать свой профиль."""
        self.client.force_authenticate(self.user)
        url = reverse("users:user-detail", kwargs={"pk": self.user.pk})
        data = {"city": "Saint Petersburg"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.city, "Saint Petersburg")

    def test_update_other_profile_forbidden(self):
        """Редактирование чужого профиля запрещено."""
        self.client.force_authenticate(self.user)
        url = reverse("users:user-detail", kwargs={"pk": self.other_user.pk})
        data = {"city": "Hacked"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_me_endpoint(self):
        """Эндпоинт /me/ возвращает текущий профиль."""
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("users:user-me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "user@test.com")
        self.assertIn("payments", response.data)
