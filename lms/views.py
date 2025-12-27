from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


# CRUD для курсов — ModelViewSet
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]


# CRUD для уроков — Generic Views
class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]
