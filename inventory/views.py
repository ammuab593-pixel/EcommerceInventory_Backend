
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product
from .serializers import ProductSerializer
from .permissions import VendorProductPermission


class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer

    permission_classes = [
        IsAuthenticated,
        VendorProductPermission
    ]

    # Search, Filter and Sorting
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    # Filter fields
    filterset_fields = [
        'category',
        'supplier',
        'price',
        'stock_quantity'
    ]

    # Search fields
    search_fields = [
        'product_name',
        'description',
        'category__category_name',
        'supplier__supplier_name'
    ]

    # Sorting fields
    ordering_fields = [
        'product_name',
        'price',
        'stock_quantity',
        'created_at'
    ]

    ordering = ['product_name']

    def get_queryset(self):

        user = self.request.user

        if user.is_superuser:
            return Product.objects.all()

        if not hasattr(user, 'profile'):
            return Product.objects.none()

        role = user.profile.role

        if role == 'admin':
            return Product.objects.all()

        elif role == 'vendor':
            return Product.objects.filter(vendor=user)

        elif role == 'end_user':
            return Product.objects.all()

        return Product.objects.none()

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)
