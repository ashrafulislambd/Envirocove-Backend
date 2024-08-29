from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Product, ProductImage, Order, Category

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(ModelSerializer):
    #vendor = UserSerializer()

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['vendor'] = UserSerializer()
        return super(ProductSerializer, self).to_representation(instance)

class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'