from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny, )
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer
    lookup_field = "slug"
    
    def serialize_tree(self, queryset):
        for obj in queryset:
            data = self.get_serializer(obj).data
            data['children'] = self.serialize_tree(obj.children.all())
            yield data

    def list(self, request):
        queryset = self.get_queryset()
        data = self.serialize_tree(queryset)
        return Response(data)

    def retrieve(self, request, pk=None):
        self.object = self.get_object()
        data = self.serialize_tree([self.object])
        return Response(data)


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny, )
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    lookup_field = "slug"

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["category__slug", "name", "description"]


class BrandView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        try:
            products = Product.objects.filter(category__slug=request.query_params['category'])
        except KeyError:
            products = Product.objects.all().order_by('brand')

        result = [product.brand for product in products]
        return Response(result)




