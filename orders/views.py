from autoparts.models import Cart, Order, Product
from django.http import JsonResponse
from rest_framework import authentication, permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from orders.serializers import OrderSerializer


class OrderItems(APIView):
    """
    Order items in the user's cart.

    * Requires token authentication.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def put(self, request, pk, *args, **kwargs):

        data = JSONParser().parse(request)

        tmp_serializer = OrderSerializer(data=data)
        if not tmp_serializer.is_valid():
            return JsonResponse(tmp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data['user_id'] = request.user.id

        try:
            order = Order.objects.filter(user_id=data['user_id'], order_id=pk)[:1].get()
            return JsonResponse({'error_detail': "this order_id already exists"}, status=status.HTTP_409_CONFLICT)
        except Order.DoesNotExist:
            order = Order(
                user_id=data['user_id'], 
                order_id=pk, 
                products=",".join(map(str, list(Cart.objects.filter(user_id=data['user_id']).values_list('product_id', flat=True)))), 
                date_time=data['date_time']
                )

        serializer = OrderSerializer(order, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

    def get(self, request, pk, format=None):
        """
        View the Order.
        """
        order = Order.objects.filter(user_id=request.user.id, order_id=pk)
        try:
            date_time = order.values_list('date_time', flat=True).first()
            items = list(Product.objects.filter(id__in=list(map(int, order.values_list('products', flat=True).first().split(",")))).values_list('name', flat=True))
            return JsonResponse({'delivery_date_time': date_time,'items': items})
        except AttributeError:
            return JsonResponse({'error_detail': "this order_id does not exist"}, status=status.HTTP_404_NOT_FOUND)

