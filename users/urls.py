from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet, RegisterView, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"payments", PaymentViewSet, basename="payment")

app_name = "users"

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
]
