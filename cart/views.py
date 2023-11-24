from django.http import JsonResponse
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient
from django.shortcuts import render
from photo.models import Photo, Category, Tag
from .models import Cart, CartItem
import json


def index(request):
    photos = Photo.objects.all()
    tags = Tag.objects.all()
    categories = Category.objects.all()
    cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    cart_items = cart.cartItems.all()
    context = {"photos": photos, "cart":cart, "cart_items":cart_items, "tags": tags, "categories": categories}
    return render (request, "cart/photo_list.html", context)

def cart(request):
    if request.user.is_authenticated:
        cart = None
        cart_items = []
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cart_items = cart.cartItems.all()
    
    context = {"cart": cart, "items": cart_items}
    return render (request, "cart/cart.html", context)


def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Photo.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cart_item, created =CartItem.objects.get_or_create(cart=cart, photo=product)
        print(cart_item)
        cart_item.quantity += 1
        cart_item.save()
        tally = cart.tally
        cart_items = list(cart.cartItems.all().values())  # Convert QuerySet to a list of dictionaries
        response_data = {"tally": tally, "cart_items": cart_items}
    return JsonResponse(response_data, safe=False)

def remove_from_cart(request):
    pass

def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    cart_items = cart.cartItems.all()
    default_phone_number = request.user.phone_number
    context = {"cart":cart, "cart_items":cart_items, "default_phone_number":default_phone_number}
    return render (request, "cart/checkout.html", context)

def payment_checkout(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)

    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = cart.user.phone_number
    amount = int(round(cart.final_price))
    account_reference = 'Picha-Safari Sandbox'
    transaction_desc = f'Payment for cart #{cart.id}'
    callback_url = 'https://picha-safari-vercel.vercel.app/api/payments/lnm/'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)

"""
{    
   "Body": {        
      "stkCallback": {            
         "MerchantRequestID": "29115-34620561-1",            
         "CheckoutRequestID": "ws_CO_191220191020363925",            
         "ResultCode": 0,            
         "ResultDesc": "The service request is processed successfully.",            
         "CallbackMetadata": {                
            "Item": [{                        
               "Name": "Amount",                        
               "Value": 1.00                    
            },                    
            {                        
               "Name": "MpesaReceiptNumber",                        
               "Value": "NLJ7RT61SV"                    
            },                    
            {                        
               "Name": "TransactionDate",                        
               "Value": 20191219102115                    
            },                    
            {                        
               "Name": "PhoneNumber",                        
               "Value": 254708374149                    
            }]            
         }        
      }    
   }
}
"""