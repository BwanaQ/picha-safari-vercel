from django.http import JsonResponse
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient
from django.shortcuts import render, redirect, get_object_or_404
from photo.models import Photo, Category, Tag
from .models import Cart, CartItem
import json
from django.contrib.auth.decorators import login_required
from payment.models import Transaction
from payment.utils import mpesa
import openpyxl as openpyxl
from django.contrib import messages
from django.conf import settings
import time
import traceback

def transform_phone_number(phone_number):
    phonenumber = str(phone_number)
    print(f"Trying ", phonenumber)
    if not phonenumber:
        return phonenumber
    if phonenumber == "":
        return phonenumber
    if phonenumber.startswith('0'):
        print("It starts with zero")
        return '254' + phonenumber[1:]
    elif phonenumber.startswith('+254'):
        return phonenumber[1:]
    else:
        return phonenumber
    
def getDetails(request, user):
    summarydictionary = {}

    # Access AUTH_USER_MODEL fields
    app_user = settings.AUTH_USER_MODEL.objects.get(id=user.id)
    firstname = app_user.first_name
    lastname = app_user.last_name
    fullname = f"{firstname} {lastname}"
    userid = app_user.id

    if app_user.isadmin:
        summarydictionary['istheadmin'] = True
    else :
        summarydictionary['istheadmin'] = False

    if request.user.is_authenticated:
        cart = None
        cart_items = []
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cart_items = cart.cartItems.all()

    try:

        summarydictionary['fullname'] = fullname
        summarydictionary['userid'] = str(userid)[:5].upper()
        summarydictionary['cart'] = cart
        summarydictionary['cart_items'] = cart_items
        summarydictionary['mobile'] = request.user.phone_number
    except Exception as exception:
        traceback_str = traceback.format_exc()
        print(f"This is the error {traceback_str}")
        pass

    return summarydictionary



@login_required(login_url='login')
def index(request):
    photos = Photo.objects.all()
    tags = Tag.objects.all()
    categories = Category.objects.all()
    cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    cart_items = cart.cartItems.all()
    context = {"photos": photos, "cart":cart, "cart_items":cart_items, "tags": tags, "categories": categories}
    return render (request, "cart/photo_list.html", context)

@login_required(login_url='login')
def cart(request):
    if request.user.is_authenticated:
        cart = None
        cart_items = []
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cart_items = cart.cartItems.all()
    
    context = {"cart": cart, "items": cart_items}
    return render (request, "cart/cart.html", context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    cart_items = cart.cartItems.all()
    default_phone_number = request.user.phone_number
    context = {"cart":cart, "cart_items":cart_items, "default_phone_number":default_phone_number}
    return render (request, "cart/checkout.html", context)

@login_required(login_url='login')
def payment_checkout(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)

    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = cart.user.phone_number
    amount = int(round(cart.final_price))
    account_reference = f'PS-#{cart.id}'
    transaction_desc = f'Checkout Payment'
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
from django.views.decorators.cache import never_cache

@never_cache
def cartbuy(request):
    gateway = mpesa.MpesaGateway()
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        user = request.user
        summarydictionary = getDetails(request, user)
        amount = int(round(cart.final_price))
        purpose= "CHECKOUT"
    else:
        return redirect('cart-home')

    mobile = cart.user.phone_number
    summarydictionary['mobile'] = mobile
    if request.method == 'POST':
        print("It is a post request")
        therequest = request.POST
        thedictionary = therequest.dict()

        print(thedictionary)

        for value in thedictionary.items():
            thestring = value[1]
            print(thestring)
            start_index = thestring.find('254')
            end_index = start_index + 12
            mobile = transform_phone_number(thestring[start_index:end_index])

        timestamp = time.time()
        gateway.stk_push_request(amount, mobile, cart, user, purpose, timestamp)

        iscomplete = False
        start_time = time.time()
        while not iscomplete and time.time() - start_time < 60:
            status = Transaction.objects.filter(timestamp=timestamp).get().status
            print(f"Checking -- {status}")
            if status == "CANCELLED" or status == "FAILED":
                iscomplete = True
                return JsonResponse({'success': False})
            elif status == "COMPLETE":
                iscomplete = True
                return JsonResponse({'success': True})

        if not iscomplete:
            return JsonResponse({'success': False})
        return JsonResponse({'success': True})

    else:
        print("It is not post")
    response = render(request, "payment.html", {"summary": summarydictionary})
    return response

