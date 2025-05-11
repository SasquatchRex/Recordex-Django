# models.py
from django.db import models
from django.contrib.auth.models import User





class Invoice(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE) # who processed the bill
    date = models.DateTimeField() # Date in which Bill is Created

    # Owner Information
    to_Name = models.TextField(max_length=200) # Name of Company
    from_PAN = models.IntegerField() # PAN number of Owner


    # Receiver Information
    from_Name = models.TextField(max_length=200) #Name of receiving Company
    to_PAN = models.IntegerField() # PAN number of receiver

    # Payment Information
    Total = models.DecimalField(max_digits=10,decimal_places=2)
    Discount_Percentage = models.DecimalField(max_digits=5,decimal_places=2)
    Taxable_Amount = models.DecimalField(max_digits=10,decimal_places=2)
    VAT_Amount = models.DecimalField(max_digits=10,decimal_places=2)
    Total_Amount = models.DecimalField(max_digits=10,decimal_places=2)
    Remarks = models.TextField(max_length=600,blank=True)

    def __str__(self):
        return f"{self.date.date()}  |   Invoice #{self.id}   |   {self.to_Name}  |   Total Amount:   {self.Total_Amount}"



class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice,related_name="Items",on_delete=models.CASCADE)
    HS_Code = models.TextField(max_length=50,blank=True,default="-")
    Name = models.TextField(max_length=200)
    Quantity = models.DecimalField(max_digits=5,decimal_places=2)
    Unit = models.TextField(max_length=50)
    Rate = models.DecimalField(max_digits=8,decimal_places=2)
    Amount = models.DecimalField(max_digits=9,decimal_places=2)

    def __str__(self):
        return f"{self.Name} | {self.Quantity} | {self.Amount}"



class Expense(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE) # who processed the bill
    date = models.DateTimeField() # Date in which Bill is Created

    # Owner Information
    to_Name = models.TextField(max_length=200) # Name of Company
    from_PAN = models.IntegerField() # PAN number of Owner


    # Receiver Information
    from_Name = models.TextField(max_length=200) #Name of receiving Company
    to_PAN = models.IntegerField() # PAN number of receiver

    # Payment Information
    Total = models.DecimalField(max_digits=10,decimal_places=2)
    Discount_Percentage = models.DecimalField(max_digits=5,decimal_places=2)
    Taxable_Amount = models.DecimalField(max_digits=10,decimal_places=2)
    VAT_Amount = models.DecimalField(max_digits=10,decimal_places=2)
    Total_Amount = models.DecimalField(max_digits=10,decimal_places=2)
    Remarks = models.TextField(max_length=600,blank=True)

    def __str__(self):
        return f"{self.date.date()}  |   Invoice #{self.id}   |   {self.to_Name}  |   Total Amount:   {self.Total_Amount}"


class ExpenseItem(models.Model):
    expense = models.ForeignKey(Expense,related_name="Items",on_delete=models.CASCADE)
    HS_Code = models.TextField(max_length=50,blank=True,default="-")
    Name = models.TextField(max_length=200)
    Quantity = models.DecimalField(max_digits=5,decimal_places=2)
    Unit = models.TextField(max_length=50)
    Rate = models.DecimalField(max_digits=8,decimal_places=2)
    Amount = models.DecimalField(max_digits=9,decimal_places=2)

    def __str__(self):
        return f"{self.Name} | {self.Quantity} | {self.Amount}"
