from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, UpdateView
from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, Product


class ListProducts(APIView):
    """
    View to list all products in the system.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all products.
        """
        products = {
            'products': [product.name for product in Product.objects.all()]
        }
        return JsonResponse(products)


class ProductDetail(APIView):
    """
    View Details of a Product
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        """
        Return a list of all products.
        """

        product = Product.objects.filter(id=pk)
        product_name = product.values_list('name', flat=True).first()
        details = product.values_list('details', flat=True).first()

        if product_name != None:
            return JsonResponse({'product_name': product_name,'details': details})
        else:
            return JsonResponse({'error_detail': "use an available product_id"}, status=status.HTTP_404_NOT_FOUND)
    
