from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from .models import User, Company

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'company')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'company', 'password'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'company', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    list_display = ('username', 'company', 'is_staff')
    search_fields = ('username',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Company)


from .models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0  # no empty rows

class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemInline]
    fields = ['creator','company','Date','to_Name','to_PAN','to_address','Total','Discount_Percentage','Taxable_Amount','VAT_Amount','Total_Amount','payment_paid','Remarks']  # This will show all fields of the Invoice model in the admin form
    # list_display = ('InvoiceNumber', 'company')
    list_filter = ('company',)
admin.site.register(Invoice, InvoiceAdmin)
