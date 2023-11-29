from django.urls import path
from .views import ProductList, AddToCart, ViewCart, CategoryList

urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('add-to-cart/', AddToCart.as_view(), name='add-to-cart'),
    path('view-cart/', ViewCart.as_view(), name='view-cart'),
]
