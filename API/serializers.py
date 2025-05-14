from rest_framework import serializers
from .models import InvoiceItem

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = [
            'id',
            'invoice',
            'HS_Code',
            'Name',
            'Quantity',
            'Unit',
            'Rate',
            'Amount'
        ]