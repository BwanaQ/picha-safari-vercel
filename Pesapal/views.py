import uuid
import requests

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from .utils import PesaPalGateway
from decouple import config

payment_url = config("PAYMENT_URL")

gateway = PesaPalGateway()

def pay(request):
    if request.method == "POST":
        phonenumber = request.POST["phone_number"]
        email = request.POST["email"]
        amount = 10.00
        currency = "KES"
        callback_url = "https://573b-197-248-239-47.ngrok-free.app/pesapal/callback" #Your callback URL

        try:
            res = gateway.make_payment(phonenumber, email, amount, currency, callback_url)
            
            redirect_url = res['redirect_url']
            return redirect(redirect_url)
        
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return HttpResponse(error_message)
        
    return render(request, 'payments.html')

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

