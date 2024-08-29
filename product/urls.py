from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views


router = DefaultRouter()

router.register("list", views.ProductViewset, basename="list")
router.register("images", views.ProductImageViewset, basename="images")
router.register("orders", views.OrderViewset, basename="orders")
router.register("categories", views.CategoryViewset, basename="categories")

urlpatterns = router.urls + [
    path("create_order/", views.create_order, name="create_order"),
]
