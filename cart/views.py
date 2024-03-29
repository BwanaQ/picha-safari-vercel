from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from decouple import config

from photo.models import Photo, Category, Tag
from .models import Cart, CartItem
from .utils import PesaPalGateway
import json
from paypal.standard.forms import PayPalPaymentsForm
import openpyxl as openpyxl
import time
import traceback
import uuid
import re
import requests

payment_url = config("PAYMENT_URL")
gateway = PesaPalGateway()


@login_required(login_url='login')
def index(request):
    photos = Photo.objects.all()
    paginator = Paginator(photos, 9)
    page_number = request.GET.get('page')
    try:
        photos = paginator.page(page_number)
    except PageNotAnInteger:
        photos=paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)    
    

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
    response_data = {}
    data = json.loads(request.body)
    product_id = data["id"]
    product = Photo.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        
        # Check if the item already exists in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, photo=product)
        if not created:
            # If the item already exists, just increment the quantity
            cart_item.quantity += 1
            cart_item.save()
        
        tally = cart.tally
        cart_items = list(cart.cartItems.all().values())  # Convert QuerySet to a list of dictionaries
        response_data = {"tally": tally, "cart_items": cart_items}

        # Send success message to the client
        success_message = f"{product.title} was added to cart successfully!"
        response_data["success_message"] = success_message

    return JsonResponse(response_data, safe=False)

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    try:
        cart = Cart.objects.get(user=request.user, completed=False)
        cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
        cart_item.delete()
        return JsonResponse({'message': 'Item removed from cart successfully.'})
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Cart not found.'}, status=404)
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'CartItem not found.'}, status=404)

@login_required(login_url='login')
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    cart_items = cart.cartItems.all()
    phone_number = request.user.phone_number
    pattern = re.compile(r'(\d{3})(\d+)(\d{2})')
    reduced_number = pattern.sub(r'\1xxxxx\3', phone_number)
    if request.method == 'POST':
        phonenumber = phone_number
        email = request.user.email
        amount = cart.final_price
        currency = "KES"
        callback_url = "https://573b-197-248-239-47.ngrok-free.app/pesapal/callback" #Edit Accordingly

        try:
            res = gateway.make_payment(phonenumber, email, amount, currency, callback_url)
            
            redirect_url = res['redirect_url']
            return redirect(redirect_url)
        
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return HttpResponse(error_message)
    
    context = {"cart":cart, "cart_items":cart_items, "reduced_number":reduced_number}
    return render (request, "cart/checkout.html", context)

@login_required(login_url='login')
def process_paypal_payment(request):
    cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    cart_items = cart.cartItems.all()
    host = request.get_host()  
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': f'{cart.final_price}',
        'item_name': f'Order # {cart.id}',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("paypal-return")}',
        'cancel_url': f'http://{host}{reverse("paypal-cancel")}',
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {'cart':cart,'cart_items':cart_items,'paypal_dict':paypal_dict,'form':form}
    return render(request,'cart/process_paypal_payment.html', context)

@csrf_exempt
def paypal_return(request):
    cart = Cart.objects.filter(user=request.user, completed=False).first()
    if cart:
        cart.completed = True
        cart.save()

    messages.success(request,"Payment was successfull.")
    return redirect("cart-home")    

@csrf_exempt
def paypal_cancel(request):
    messages.error(request,"Failed! Payment was cancelled.")
    return redirect("cart-home")    


def paymentIPN(request):
    orderTrackingId = request.GET.get("OrderTrackingId")
    orderMerchantReference = request.GET.get("OrderMerchantReference")
    orderNotificationType = request.GET.get("OrderNotificationType")

    payment_url = f"https://cybqa.pesapal.com/pesapalv3/api/Transactions/GetTransactionStatus?orderTrackingId={orderTrackingId}"

    token = gateway.getAuthorizationToken()

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer %s" % token,
        "Accepts": "application/json"
    }
    payment_status = requests.get(payment_url, headers=headers)


    return JsonResponse(payment_status.json())


def callback(request):
    return HttpResponse("Successs")
