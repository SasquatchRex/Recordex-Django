from django.urls import path
from . import views
from . import Authentication
from . import Invoice,expense

urlpatterns = [
    # Authentication
    path('login/', Authentication.login_view),
    path('logout/', Authentication.logout_view),
    path('checklogin/', Authentication.check_user_login),
    path('checktoken/',Authentication.check_token),

    # Invoice
    path('create/invoice/',Invoice.create_invoice),
    path('invoices/',Invoice.invoice_list),
    path('invoice/bill/<str:pk>/',Invoice.billGenerator),
    path('invoice/preview/',Invoice.billPreview),
    # path('invoice/',Invoice.InvoiceItem),

    #Expense
    path('create/expense/',expense.create_expense),
    path('expesne/',expense.expense_list),
]