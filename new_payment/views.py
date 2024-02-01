from django.shortcuts import render
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient

# Create your views here.
def index(request):
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '0720935434'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    # callback_url = 'https://darajambili.herokuapp.com/express-payment';
    callback_url = 'https://picha-safari-vercel.vercel.app/new-payment/daraja/stk_push/'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)

def stk_push_callback(request):
        data = request.body
        print(data)
        return HttpResponse(data)