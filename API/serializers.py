from rest_framework import serializers
from .models import ExpenseItem,InvoiceItem

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


class ExpenseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseItem
        fields = [
            'id',
            'expense',
            'HS_Code',
            'Name',
            'Quantity',
            'Unit',
            'Rate',
            'Amount'
        ]