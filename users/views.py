from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, serializers, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Payment
from .permissions import IsOwner
from .serializers import PaymentSerializer, RegisterSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет пользователей."""

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve" and self.request.user != self.get_object():
            return PublicUserSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == "me":
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]


class PublicUserSerializer(serializers.ModelSerializer):
    """Публичный профиль без чувствительных данных."""

    class Meta:
        model = User
        fields = ("id", "email", "phone", "city", "avatar", "date_joined")


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет платежей с фильтрацией и сортировкой."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["course", "lesson", "payment_method"]
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]


class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя."""

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
