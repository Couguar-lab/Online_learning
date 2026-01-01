from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from lms.models import Course, Subscription
from django.urls import reverse

User = get_user_model()


class SubscriptionTests(APITestCase):
    """Тесты функционала подписки на курс."""

    def setUp(self):
        self.user = User.objects.create_user(email='sub@test.com', password='pass123')
        self.course = Course.objects.create(title='Sub Course', owner=self.user)
        self.client = APIClient()

    def test_subscribe_and_unsubscribe(self):
        """Пользователь может подписаться и отписаться от курса."""
        self.client.force_authenticate(self.user)
        url = reverse('lms:subscribe')
        data = {'course_id': self.course.id}

        # Подписка
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # Отписка
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscribe_non_existent_course(self):
        """Ошибка при подписке на несуществующий курс."""
        self.client.force_authenticate(self.user)
        url = reverse('lms:subscribe')
        data = {'course_id': 999}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)