from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.permissions import IsModerator, IsOwner

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .paginators import LMSPagination


# CRUD для курсов — ModelViewSet
class CourseViewSet(viewsets.ModelViewSet):
    """CRUD для курсов с разграничением прав."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LMSPagination

    def get_permissions(self):
        """Динамические права в зависимости от действия."""
        if self.action in ["create"]:
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Автоматическая привязка курса к создателю."""
        serializer.save(owner=self.request.user)


# CRUD для уроков — Generic Views
class LessonListCreateView(generics.ListCreateAPIView):
    """Список и создание уроков (только не-модераторы могут создавать)."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]
    pagination_class = LMSPagination

    def perform_create(self, serializer):
        """Привязка урока к авторизованному пользователю."""
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, обновление и удаление урока (владелец или модератор)."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class SubscriptionView(APIView):
    """Управление подпиской на курс (POST — toggle)."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response({"message": message})