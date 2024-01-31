from mpesa.models import LNMOnline
from mpesa.api.serializers import LNMOnlineSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from cart.models import Cart 

from django.shortcuts import redirect
from django.contrib import messages
from datetime import datetime
import pytz
class LNMCallbackUrlAPIView(CreateAPIView):
    queryset = LNMOnline.objects.all()
    serializer_class = LNMOnlineSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        print(request.data, "this is request.data")
        merchant_request_id = request.data["Body"]["stkCallback"]["MerchantRequestID"]
        checkout_request_id = request.data["Body"]["stkCallback"]["CheckoutRequestID"]
        result_code = request.data["Body"]["stkCallback"]["ResultCode"]
        result_description = request.data["Body"]["stkCallback"]["ResultDesc"]
        amount = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
        mpesa_receipt_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"]
        balance = ""
        transaction_date = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][3]["Value"]
        phone_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]
        str_transaction_date = str(transaction_date)
        transaction_datetime = datetime.strptime(str_transaction_date, "%Y%m%d%H%M%S")
        aware_transaction_datetime = pytz.utc.localize(transaction_datetime)

        our_model = LNMOnline.objects.create(
            cart=cart,
            CheckoutRequestID=checkout_request_id,
            MerchantRequestID=merchant_request_id,
            Amount=amount,
            ResultCode=result_code,
            ResultDesc=result_description,
            MpesaReceiptNumber=mpesa_receipt_number,
            Balance=balance,
            TransactionDate=aware_transaction_datetime,
            PhoneNumber=phone_number,
        )
        our_model.save()
        if result_code == "0":
            # Set cart.completed to true
            cart.completed = True
            cart.save()

            # Redirect to the home page with a success message
            messages.success(request, 'Checkout was successful!')
            return redirect('cart-home')  # Replace 'home' with the actual URL name or path of your home page

        else:
            # Return to home page with a failure message
            messages.error(request, 'Checkout was not successful.')
            return redirect('cart-home')  # Replace 'home' with the actual URL name or path of your home page
