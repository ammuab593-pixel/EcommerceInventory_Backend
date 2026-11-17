
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartItem
from .serializers import CartSerializer
from inventory.models import Product


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        product_id = request.data.get('product')

        try:
            quantity = int(request.data.get('quantity', 1))
            if quantity < 1:
                raise ValueError
        except (TypeError, ValueError):
            return Response(
                {"error": "Quantity must be a positive number."},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = get_object_or_404(
            Product.objects.select_for_update(),
            id=product_id
        )

        if product.stock_quantity == 0:
            return Response(
                {"error": "Product is sold out."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity > product.stock_quantity:
            return Response(
                {
                    "error": f"Only {product.stock_quantity} products are available."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()

        product.stock_quantity -= quantity
        product.save(update_fields=['stock_quantity'])

        return Response(
            {
                "message": "Product added to cart successfully.",
                "remaining_stock": product.stock_quantity,
                "cart": CartSerializer(cart).data
            },
            status=status.HTTP_200_OK
        )


class ViewCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK
        )


class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def patch(self, request, item_id):
        cart = get_object_or_404(
            Cart.objects.select_for_update(),
            user=request.user
        )

        item = get_object_or_404(
            CartItem.objects.select_for_update(),
            id=item_id,
            cart=cart
        )

        try:
            quantity = int(request.data.get('quantity'))
            if quantity < 1:
                raise ValueError
        except (TypeError, ValueError):
            return Response(
                {"error": "Enter a valid positive quantity."},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = get_object_or_404(
            Product.objects.select_for_update(),
            id=item.product_id
        )

        difference = quantity - item.quantity

        if difference > product.stock_quantity:
            return Response(
                {
                    "error": f"Only {product.stock_quantity} additional products are available."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        product.stock_quantity -= difference
        product.save(update_fields=['stock_quantity'])

        item.quantity = quantity
        item.save(update_fields=['quantity'])

        return Response(
            {
                "message": "Cart quantity updated.",
                "remaining_stock": product.stock_quantity,
                "cart": CartSerializer(cart).data
            },
            status=status.HTTP_200_OK
        )


class RemoveCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def delete(self, request, item_id):
        cart = get_object_or_404(
            Cart.objects.select_for_update(),
            user=request.user
        )

        item = get_object_or_404(
            CartItem.objects.select_for_update(),
            id=item_id,
            cart=cart
        )

        product = get_object_or_404(
            Product.objects.select_for_update(),
            id=item.product_id
        )

        product.stock_quantity += item.quantity
        product.save(update_fields=['stock_quantity'])

        item.delete()

        return Response(
            {
                "message": "Product removed from cart.",
                "restored_stock": product.stock_quantity
            },
            status=status.HTTP_200_OK
        )
