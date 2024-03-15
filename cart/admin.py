from django.contrib import admin
from .models import Cart, CartItem, Transaction

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Transaction)