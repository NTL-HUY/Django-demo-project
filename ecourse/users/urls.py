from django.urls import include, path

from users.views import UserView


urlpatterns = [
    path("login",UserView.login),
    path("auth/google/", UserView.google_login),
    path("auth/google/callback/", UserView.google_callback),
]