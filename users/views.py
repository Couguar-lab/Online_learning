from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .serializers import UserSerializer

User = get_user_model()


# Основной ViewSet для всех пользователей
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # Чтение — всем, изменение — только аутентифицированным

    # Специальный эндпоинт /api/users/me/
    @action(
        detail=False,
        methods=["get", "patch", "put"],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if request.method in ["PATCH", "PUT"]:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer.is_valid()
        return Response(serializer.data)
