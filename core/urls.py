from django.urls import path
from . import views

urlpatterns = [
    path("profile", views.profile, name="profile"),
    path("set_type", views.set_type, name="set_type"),
    path("set_shipping_address", views.set_shipping_address, name="set_shipping_address"),
    path("demo_login", views.demo_login, name="demo_login"),
    path("google", views.GoogleLogin.as_view(), name='google_login'),
]
