from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Expense, ExpenseItem
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.dateparse import parse_date
from django.http import JsonResponse

from decimal import Decimal


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_expense_invoice(request):
    data = request.data

    with transaction.atomic():
        invoice = Expense.objects.create(
            creator = request.user,
            date = data["Date"],

            to_Name = data["To Name"],
            to_PAN = data["To PAN"],
            from_Name = data["From Name"],
            from_PAN = data["From PAN"],

            Total=Decimal(data['Total']),
            VAT_Amount=Decimal(data['VAT Amount']),
            Discount_Percentage=Decimal(data['Discount Percentage']),
            Total_Amount=Decimal(data['Total Amount']),
            Taxable_Amount = Decimal(data['Taxable Amount']),
            Remarks=data['Remarks']
        )

        for item in data['Invoice Items']:
            ExpenseItem.objects.create(
                invoice=invoice,
                HS_Code=item.get('H.S Code'),
                Name=item['Name'],
                Quantity=Decimal(item['Quantity']),
                Rate=Decimal(item['Rate']),
                Unit = item['Unit'],
                Amount=Decimal(item['Amount'])
            )

    return Response({'message': 'Invoice created successfully'},status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expense_list(request):
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    expenses = Expense.objects.all()

    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
        if from_date and to_date:
            expenses = expenses.filter(date__range=(from_date, to_date))


    data = [
        {
            "id": invoice.id,
            "creator": invoice.creator.username if invoice.creator else None,
            "date": str(invoice.date.date()),
            "To Name": invoice.to_Name,
            "To PAN" : invoice.to_PAN,

            "From Name" : invoice.from_Name,
            "From PAN" : Decimal(invoice.from_PAN),

            "Total" : Decimal(invoice.Total),
            "VAT Amount" : Decimal(invoice.VAT_Amount),
            "Discount Percentage" : Decimal(invoice.Discount_Percentage),
            "Total Amount" : Decimal(invoice.Total_Amount),
            "Taxable Amount" : Decimal(invoice.Taxable_Amount),
            "Remarks": str(invoice.Remarks),

            # "items" : [{
            #     "HS Code" :item.HS_Code,
            #     "Name" : str(item.Name),
            #     "Quantity" : Decimal(item.Quantity),
            #     "Rate": Decimal(item.Rate),
            #     "Unit": str(item.Unit),
            #     "Amount": Decimal(item.Amount)
            #
            # }
            # for item in invoice.Items.all()
            # ]

        }
        for invoice in expenses
    ]

    return JsonResponse(data, safe=False)









