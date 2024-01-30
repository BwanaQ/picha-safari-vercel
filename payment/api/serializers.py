from rest_framework import serializers

from payment.models import *


class MpesaCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['cart']


    def validate(self, data):
        cart = data.get('cart')
        mobile = data.get('mobile')
        amount = data.get('amount')
        timestamp = data.get('timestamp')

        if not cart:
            raise serializers.ValidationError('Cart is required')
        if not amount:
            raise serializers.ValidationError('Amount is required')
        if not mobile:
            raise serializers.ValidationError('Mobile is required')
        if not timestamp:
            raise serializers.ValidationError('Timestamp is required')

        return data