from django.urls import path
from . import views

urlpatterns = [
    path("profile", views.profile, name="profile"),
    path("set_type", views.set_type, name="set_type"),
    path("set_shipping_address", views.set_shipping_address, name="set_shipping_address"),
    path("store_info", views.store_info, name="store_info"),
    path("set_store_info", views.set_store_info, name="set_store_info"),
    path("demo_login", views.demo_login, name="demo_login"),
    path("google", views.GoogleLogin.as_view(), name='google_login'),
]
