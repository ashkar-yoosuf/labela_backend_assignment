from autoparts.models import Cart
from rest_framework import serializers


class CartSerializer(serializers.Serializer):
    
    user_id = serializers.IntegerField(required=False)
    product_id = serializers.IntegerField(required=True)
    product_name = serializers.CharField(required=False)
    quantity = serializers.IntegerField(required=True)

    def create(self, validated_data):
        """
        Create and return a new `Cart` instance, given the validated data.
        """
        return Cart.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Cart` instance, given the validated data.
        """
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.product_id = validated_data.get('product_id', instance.product_id)
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance
