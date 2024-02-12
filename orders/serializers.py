from autoparts.models import Order
from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    
    user_id = serializers.IntegerField(required=False)
    order_id = serializers.IntegerField(required=False)
    products = serializers.CharField(required=False)
    date_time = serializers.DateTimeField(required=True)


    def create(self, validated_data):
        """
        Create and return a new `Order` instance, given the validated data.
        """
        return Order.objects.create(**validated_data)


    def update(self, instance, validated_data):
        """
        Update 'Order' instance.
        """
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.order_id = validated_data.get('order_id', instance.order_id)
        instance.products = validated_data.get('products', instance.products)
        instance.date_time = validated_data.get('date_time', instance.date_time)

        instance.save()
        return instance
