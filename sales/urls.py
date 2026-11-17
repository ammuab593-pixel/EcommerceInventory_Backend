
from django.urls import path

from .views import (
    AddToCartView,
    ViewCartView,
    UpdateCartItemView,
    RemoveCartItemView,
)

urlpatterns = [
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', ViewCartView.as_view(), name='view_cart'),
    path('cart/update/<int:item_id>/', UpdateCartItemView.as_view(), name='update_cart'),
    path('cart/remove/<int:item_id>/', RemoveCartItemView.as_view(), name='remove_cart'),
]
