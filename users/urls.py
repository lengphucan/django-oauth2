from django.urls import path

from users.views import (
    RegisterView,
    UserDetailView,
)


urlpatterns = [
    path("user-detail", UserDetailView.as_view(), name="user-detail"),
    path("register", RegisterView.as_view(), name="register"),
    # path("login", LoginView.as_view(), name="login"),
    # path("get", GetUserView.as_view(), name="get"),
]
