from django.contrib import admin

# Register your models here.
from mpesa.models import LNMOnline


class LNMOnlineAdmin(admin.ModelAdmin):
    list_display = ("PhoneNumber", "Amount", "MpesaReceiptNumber", "TransactionDate")

admin.site.register(LNMOnline,LNMOnlineAdmin)
