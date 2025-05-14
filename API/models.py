from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Company(models.Model):
    Construction = 'Construction'
    Shop = 'Shop'
    COMPANY_TYPES = [
        (Construction, 'Construction Company. Eg-GDC'),
        (Shop, 'Shop Company. Eg- DnD'),
    ]

    name = models.CharField(max_length=100)
    shortName = models.CharField(max_length=10)
    type = models.CharField(max_length=30, choices=COMPANY_TYPES)

    def __str__(self):
        return f'{self.name} | {self.type}'


class User(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True, blank=True)


class Invoice(models.Model):
    InvoiceNumber = models.CharField(max_length=20, primary_key=True, editable=False)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)

    creator = models.ForeignKey(User, on_delete=models.CASCADE) # who processed the bill
    Date = models.DateField() # TRANSACTION DATE & BILLED DATE SHOULD BE SEPARATED


    payment_paid = models.BooleanField(default=True)


    # Receiver Information

    to_Name = models.CharField(max_length=200)  # Name of Company
    to_PAN = models.IntegerField() # PAN number of receiver
    to_address = models.CharField(max_length=100,blank=True,default="") # address of receiver




    # Payment Information
    Total = models.DecimalField(max_digits=10,decimal_places=2)
    Discount_Percentage = models.DecimalField(max_digits=5,decimal_places=2)
    Taxable_Amount = models.DecimalField(max_digits=10,decimal_places=2)
    VAT_Amount = models.DecimalField(max_digits=10,decimal_places=2)
    Total_Amount = models.DecimalField(max_digits=10,decimal_places=2)
    Remarks = models.CharField(max_length=600,blank=True)

    def __str__(self):
        return f"{self.Date}  |   Invoice #{self.InvoiceNumber}   |   {self.to_Name}  |   Total Amount:   {self.Total_Amount}"

    def save(self, *args, **kwargs):
        if not self.pk:
            prefix = self.company.shortName.upper()
            last_invoice = Invoice.objects.filter(company=self.company).order_by('-Date').first()
            if last_invoice:
                last_number = int(last_invoice.number.split('-')[-1])
                next_number = f"{last_number + 1:05d}"
            else:
                next_number = "00001"
            self.InvoiceNumber = f"{prefix}-{next_number}"
        super().save(*args, **kwargs)

    # @property
    # def bs_created_at(self):
    #     return nepali_datetime.date.from_datetime_date(self.Date)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice,related_name="Items",on_delete=models.CASCADE)
    HS_Code = models.CharField(max_length=50,blank=True,default="-")
    Name = models.CharField(max_length=200)
    Quantity = models.DecimalField(max_digits=5,decimal_places=2)
    Unit = models.CharField(max_length=50)
    Rate = models.DecimalField(max_digits=8,decimal_places=2)
    Amount = models.DecimalField(max_digits=9,decimal_places=2)

    def __str__(self):
        return f"{self.Name} | {self.Quantity} | {self.Amount}"
