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

from photo.models import Photo, Category, Tag
from .models import Cart, CartItem
import json
from paypal.standard.forms import PayPalPaymentsForm
import openpyxl as openpyxl
import time
import traceback
import uuid

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

        # Send success message to the client
        success_message = f"{cart_item.photo.title} was added to cart successfully!"
        response_data["success_message"] = success_message

    return JsonResponse(response_data, safe=False)

@login_required(login_url='login')
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
    messages.success("Payment was successfull.")
    return redirect("cart-home")    

@csrf_exempt
def paypal_cancel(request):
    messages.error("Failed! Payment was cancelled.")
    return redirect("cart-home")    
