from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course

User = get_user_model()


class CourseTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@test.com", password="pass")
        self.moderator = User.objects.create_user(email="mod@test.com", password="pass")
        self.moderator.groups.create(name="moderators")
        self.course = Course.objects.create(title="My Course", owner=self.user)

    def test_create_course_as_owner(self):
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/courses/", {"title": "New Course"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_course_as_moderator_forbidden(self):
        self.client.force_authenticate(self.moderator)
        response = self.client.post("/api/courses/", {"title": "Forbidden"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
