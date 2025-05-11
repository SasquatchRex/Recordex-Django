from django.urls import path
from . import views
from . import Authentication
from . import Invoice

urlpatterns = [
    # Authentication
    path('login/', Authentication.login_view),
    path('signup/', Authentication.signup),
    path('logout/', Authentication.logout_view),
    path('checklogin/', Authentication.check_user_login),
    path('checktoken/',Authentication.check_token),

    # Invoice
    path('create/invoice/',Invoice.create_invoice),
    path('invoices/',Invoice.invoice_list),
    path('invoice/bill/<int:pk>/',Invoice.billGenerator)
    # path('invoice/',Invoice.InvoiceItem),
]