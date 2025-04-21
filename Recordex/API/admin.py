from django.contrib import admin
from .models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0  # no empty rows

class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemInline]
    fields = ['creator','date','to_Name','from_PAN','from_Name','to_PAN','Total','Discount_Percentage','Taxable_Amount','VAT_Amount','Total_Amount','Remarks']  # This will show all fields of the Invoice model in the admin form

admin.site.register(Invoice, InvoiceAdmin)
