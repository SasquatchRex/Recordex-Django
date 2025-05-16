
from rest_framework.response import Response
from .models import Company,Expense,ExpenseItem
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from decimal import Decimal



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_expense(request):
    data = request.data


    with transaction.atomic():
        expense = Expense.objects.create(
            creator = request.user,
            company = request.user.company,
            Date = data["Date"],
            payment_paid = data["Payment Paid"],

            from_Name = data["From Name"],
            from_PAN = data["From PAN"],
            # to_address = data["Address"],
            # to_Name = data["From Name"],
            # to_PAN = data["From PAN"],

            Total=Decimal(data['Total']),
            VAT_Amount=Decimal(data['VAT Amount']),
            Discount_Percentage=Decimal(data['Discount Percentage']),
            Total_Amount=Decimal(data['Total Amount']),
            Taxable_Amount = Decimal(data['Taxable Amount']),
            Remarks=data['Remarks']
        )

        for item in data['Expense Items']:
            ExpenseItem.objects.create(
                expense=expense,
                HS_Code=item.get('H.S Code'),
                Name=item['Name'],
                Quantity=Decimal(item['Quantity']),
                Rate=Decimal(item['Rate']),
                Unit = item['Unit'],
                Amount=Decimal(item['Amount'])
            )

    return Response({'message': 'Expense created successfully','Expense Number': Expense.ExpenseId},status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expense_list(request):
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    expenses = Expense.objects.filter(company = request.user.company)

    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
        if from_date and to_date:
            expenses = expenses.filter(date__range=(from_date, to_date))


    data = [
        {
            "Expense Id": expense.ExpenseId,
            "creator": expense.creator.username if expenses.creator else None,
            "date": str(expense.Date),
            "From Name": expense.from_Name,
            "From PAN" : expense.from_PAN,

            # "From Name" : invoice.from_Name,
            # "From PAN" : Decimal(invoice.from_PAN),

            "Total" : Decimal(expense.Total),
            "VAT Amount" : Decimal(expense.VAT_Amount),
            "Discount Percentage" : Decimal(expense.Discount_Percentage),
            "Total Amount" : Decimal(expense.Total_Amount),
            "Taxable Amount" : Decimal(expense.Taxable_Amount),
            "Remarks": str(expense.Remarks),
            "Payment Paid": bool(expense.payment_paid)

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
        for expense in expenses
    ]

    return JsonResponse(data, safe=False)


# def totalExpensethisMonth(request):
#     expenses = Expense.objects.filter(company=request.user.company)



















