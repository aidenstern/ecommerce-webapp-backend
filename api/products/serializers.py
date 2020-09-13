from rest_framework import serializers

from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "parent", "children", "slug")



class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length = None, use_url=True)
    
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "quantity",
            "featured",
            "description",
            "slug",
            "available",
            "category",
            "brand",
            "image",
        )
        lookup_field = "slug"
