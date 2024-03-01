from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from photo.models import Photo, Category, Tag
from .models import Cart, CartItem
import json
from django.contrib.auth.decorators import login_required

import openpyxl as openpyxl
from django.contrib import messages
from django.conf import settings
import time
import traceback
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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


