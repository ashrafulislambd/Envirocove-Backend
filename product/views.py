from django.db import transaction, IntegrityError
from django.db.models import F
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.permissions import ReadOnly, IsVendor
from core.utils import throw_unauthenticated
from .serializers import ProductSerializer, ProductImageSerializer, OrderSerializer, CategorySerializer
from .models import Product, Order, OrderItem, ProductImage, Category

import traceback

class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsVendor | ReadOnly]

    def get_queryset(self):
        query_set = super().get_queryset()
        if "vendor" in self.request.GET:
            vendor = self.request.GET["vendor"]
            query_set = query_set.filter(vendor__id=vendor)
        if "cat_id" in self.request.GET:
            cat_id = self.request.GET["cat_id"]
            query_set = query_set.filter(category=cat_id)
        return query_set


class ProductImageViewset(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsVendor | ReadOnly]

    def get_queryset(self):
        query_set = super().get_queryset()
        if "product_id" in self.request.GET:
            product_id = self.request.GET["product_id"]
            query_set = query_set.filter(product__id=product_id)
        return query_set
    
class CategoryViewset(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly]

class OrderViewset(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated & ReadOnly]

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(user=self.request.user)
    
@api_view(http_method_names=["POST"])
def create_order(request):
    shortage = False
    available = {}
    try:
        res = throw_unauthenticated(request)
        if res: return res
        cart = request.data["cart"]

        for id in cart:
            qty = cart[id]
            product = Product.objects.get(id=id)
            if product.quantity < qty:
                shortage = True
                available[id] = product.quantity

        if shortage:
            return Response({
                "error": "Some items are less in stock than the demand",
                "shortage_items_availability": available,
            })

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user = request.user
                )
                order_items = []
                for id in cart:
                    qty = cart[id]
                    product = Product.objects.get(id=id)
                    order_items.append(OrderItem(
                        order = order,
                        item = product,
                        quantity = qty,
                    ))
                    product.quantity = F("quantity") - qty
                    product.save()
                OrderItem.objects.bulk_create(order_items)

                return Response({
                    "message": "success",
                    "order_id": order.id,
                })

        except IntegrityError:
            traceback.print_exc()
            return Response({
                "error": "There was a problem handling your request."
            })
    except Product.DoesNotExist:
        return Response({
            "error": "There exists invalid product id(s) in your request"
        })
    except:
        return Response({
            "error": "There was a problem handling your request"
        })
