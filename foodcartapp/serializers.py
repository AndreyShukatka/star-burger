from rest_framework import serializers
from foodcartapp.models import Order, OrderElement
from django.db import transaction


class OrderElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderElement
        fields = ['quantity', 'product']

    @transaction.atomic
    def create(self, validated_data):
        return OrderElement.objects.create(**validated_data)


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    products = OrderElementSerializer(
        many=True, allow_empty=False, write_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id',
            'address',
            'firstname',
            'lastname',
            'phonenumber',
            'products'
        ]
