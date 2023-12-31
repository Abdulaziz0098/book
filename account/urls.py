from django.urls import path

from . import views

urlpatterns = [
    path("user/register/", views.register_api, name="register"),
    path("user/login/", views.login_api, name="login"),
    path("user/me/", views.user_api, name="me"),
    path("user/logout/", views.logout_api, name="logout"),
    path("user/profile/", views.user_profile, name="user_profile"),
    path("user/verify-email", views.verify_email, name="verify_ email"),
]
