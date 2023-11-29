from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.contrib.sessions.models import Session
from django.contrib.auth.models import AnonymousUser
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .serializers import AddToCartSerializer

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AddToCart(generics.CreateAPIView):
    serializer_class = AddToCartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        product = get_object_or_404(Product, pk=product_id)
        print(request.session)

        if 'cart' not in request.session:
            request.session['cart'] = {}

        cart = request.session['cart']
        print(cart)

        if product_id in cart:
            cart[product_id]['quantity'] += int(quantity)
        else:
            cart[product_id] = {'quantity': int(quantity), 'name': product.name, 'price': float(product.price)}

        request.session.modified = True

        return Response({'status': 'success', 'cart': request.session['cart']})

class ViewCart(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})
        total_price = sum(item['quantity'] * item['price'] for item in cart.values())
        print(cart)

        response_data = {'cart': cart, 'total_price': total_price}
        return Response(response_data)
