from django.urls import path

from . import views

urlpatterns = [
    path("user/register/", views.RegisterApi.as_view(), name="register"),
    path("user/login/", views.LoginApi.as_view(), name="login"),
    path("user/me/", views.UserApi.as_view(), name="me"),
    path("user/logout/", views.LogoutApi.as_view(), name="logout"),
]