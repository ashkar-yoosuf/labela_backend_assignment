from autoparts.models import Cart, Product
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import authentication, permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from carts.serializers import CartSerializer


class CartAction(APIView):
    """
    View to list all products in the cart of the user.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all products in the cart.
        """
        items_list = [[item.product_id, item.product_name, item.quantity] for item in Cart.objects.filter(user_id=request.user.id)]
        items = {'description':[]}
        for i in items_list:
            items['description'].append({'product_id': i[0], 'product_name': i[1], 'quantity': i[2]})

        return JsonResponse(items)


    def put(self, request, *args, **kwargs):
        """
        Add item to the user's cart.
        """

        data = JSONParser().parse(request)

        tmp_serializer = CartSerializer(data=data)
        if not tmp_serializer.is_valid():
            return JsonResponse(tmp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        available_product_ids = set(Product.objects.all().values_list('id', flat=True))
        if data['product_id'] not in available_product_ids:
            return JsonResponse({},status=status.HTTP_404_NOT_FOUND)

        data['user_id'] = request.user.id
        data['product_name'] = Product.objects.values_list('name', flat=True).filter(id=data['product_id']).first()

        try:
            item = Cart.objects.filter(product_id=data['product_id'], user_id=request.user.id)[:1].get()
        except Cart.DoesNotExist:
            item = Cart(user_id=data['user_id'], product_id=data['product_id'], product_name=data['product_name'], quantity=data['quantity'])

        serializer = CartSerializer(item, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)


class DeleteItem(APIView):
    """
    Delete item from user's cart.

    * Requires token authentication.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):

        try:
            item = Cart.objects.filter(product_id=pk, user_id=request.user.id)[:1].get()
        except Cart.DoesNotExist:
            return Response({'error_detail': "this product is not available in the cart"}, status=status.HTTP_404_NOT_FOUND)
        
        item.delete()
        return Response({'detail': "item removed"}, status=status.HTTP_204_NO_CONTENT)
