import base64
import math
import time
from datetime import datetime

import requests
from phonenumber_field.phonenumber import PhoneNumber
from requests.auth import HTTPBasicAuth
from rest_framework import serializers
from rest_framework.response import Response

from decouple import config

from cart.models import Cart
from payment.models import Transaction

class Decorators:
    @staticmethod
    def refresh_token(decorated):
        def wrapper(gateway, *args, **kwargs):
            if (
                    gateway.access_token_expiration
                    and time.time() > gateway.access_token_expiration
            ):
                token = gateway.get_access_token()
                gateway.access_token = token
            return decorated(gateway, *args, **kwargs)

        return wrapper

class MpesaGateway:
    shortcode = None
    consumer_key = None
    consumer_secret = None
    access_token_url = None
    access_token = None
    access_token_expiration = None
    checkout_url = None
    timestamp = None


    def __init__(self):
        self.headers = None
        self.access_token_expiration = None
        self.shortcode = config('MPESA_SHORTCODE')
        self.consumer_key = config('MPESA_CONSUMER_KEY')
        self.passkey = config('MPESA_PASSKEY')
        self.consumer_secret =  config('MPESA_CONSUMER_SECRET')
        self.password = self.generate_password()
        self.c2b_callback = 'https://picha-safari-vercel.vercel.app/payments/callback/'
        self.access_token_url = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        self.checkout_url = 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

        try:
            self.access_token = self.get_access_token()
            if self.access_token is None:
                raise Exception("Request for access token failed.")
        except Exception as e:
            pass
        else:
            self.access_token_expiration = time.time() + 3400


    def generate_password(self):
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = self.shortcode + self.passkey + self.timestamp
        password_byte = password.encode("ascii")
        return base64.b64encode(password_byte).decode("utf-8")

    def get_access_token(self):
        try:
            res = requests.get(self.access_token_url, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret))
        except Exception as e:
            raise e

        token = res.json()['access_token']
        self.headers = {"Authorization": "Bearer %s" % token}
        return token
    

    @Decorators.refresh_token
    def stk_push_request(self, request, amount, mobile, cart, user, purpose, timestamp):
        cart = None
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user, completed=False)

        body = {
            "BusinessShortCode": self.shortcode,
            "Password": self.password,
            "Timestamp": self.timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": math.ceil(float(amount)),
            "PartyA": mobile,
            "PartyB": self.shortcode,
            "PhoneNumber": mobile,
            "CallBackURL": self.c2b_callback,
            "account_reference": f'PS-#{cart.id}',
            "transaction_desc": f'Checkout Payment',
            "headers": self.headers
        }

        try:
            res = requests.post(self.checkout_url, json=body, headers=self.headers, timeout=30)
            res_data = res.json()
            if res.ok:
                cart = None
                if request.user.is_authenticated:
                    cart, created = Cart.objects.get_or_create(user=request.user, completed=False)


                transaction = Transaction.objects.create(
                    mobile = mobile,
                    user = user,
                    amount = cart.final_price,
                    cart = cart,
                    purpose = purpose,
                    checkoutid=res_data["CheckoutRequestID"],
                    timestamp=timestamp
                )
                transaction.save()

                data = {}

                data['details'] = "Payment was successful"
                return Response(data)

            else:
                raise Exception(f"{str(res_data['errorMessage'])}")
        except Exception as e:
            raise Exception(e)


    @staticmethod
    def check_status(data):
        try:
            status = data["Body"]["stkCallback"]["ResultCode"]
        except Exception as e:
            status = 1
        return status
    

    @staticmethod
    def getTransactionObjectWithSimilarCheckoutRequestId(data):
        checkout_request_id = data["Body"]["stkCallback"]["CheckoutRequestID"]
        transaction, _ = Transaction.objects.get_or_create(checkoutid=checkout_request_id)
        return transaction
    


    def callback(self, data):
        status = self.check_status(data)
        transaction = self.getTransactionObjectWithSimilarCheckoutRequestId(data)

        if not transaction:
            checkout_request_id = data["Body"]["stkCallback"]["CheckoutRequestID"]
            raise Exception(f"Transaction with reference Id {checkout_request_id} not found!")

        amount = 0
        phone_number = 0
        receiptnumber = 0

        if status == 0:
            items = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
            for item in items:
                if item["Name"] == "Amount":
                    amount = item["Value"]
                elif item["Name"] == "MpesaReceiptNumber":
                    receiptnumber = item["Value"]
                elif item["Name"] == "PhoneNumber":
                    phone_number = item["Value"]        
            if  transaction.purpose == "CHECKOUT":
                cart = transaction.cart
                cart.iscomplete = True
                cart.save()
            user = transaction.user
            if user:
                user.is_active = True
                user.save()    
            transaction.amount = amount
            transaction.reference = receiptnumber
            transaction.mobile = PhoneNumber(raw_input=phone_number)
            transaction.receiptnumber = receiptnumber
            transaction.status = "COMPLETE"


        elif status == 1032:
            transaction.status = "CANCELLED"
        else:
            transaction.status = "FAILED"


        transaction.save()
        return True