from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.api.serializers import MpesaCheckoutSerializer
from payment.models import Transaction
from payment.utils import mpesa
from cart.models import Cart


gateway = mpesa.MpesaGateway()

class MpesaCallBackView(APIView):

    @csrf_exempt
    def post(self, request):
        data = request.data
        respose = gateway.callback(data)
        if respose:
            return Response({"details": "Success"}, status=status.HTTP_200_OK)
        return Response({"details": "Failed"}, status=status.HTTP_400_BAD_REQUEST)


class MpesaCheckoutView(generics.CreateAPIView):

    serializer_class = MpesaCheckoutSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            try:
                self.perform_create(serializer)
            except Exception as exception:
                return Response({"details": str(exception)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"details": "Success: An Mpesa request has been sent to your mobile."}, status=status.HTTP_201_CREATED)

        else:
            errors = serializer.errors
            return Response({"details": errors}, status=status.HTTP_400_BAD_REQUEST)


    def perform_create(self, serializer):
        mobile = serializer.validated_data['mobile']
        cart = serializer.validated_data['cart']
        amount = serializer.validated_data['amount']
        purpose = serializer.validated_data['purpose']
        timestamp = serializer.validated_data['timestamp']
        loggedinuser = self.request.user.id
        serializer.validated_data['user'] = loggedinuser

        gateway.stk_push_request(amount, mobile, cart, loggedinuser, purpose, timestamp)



class PaymentListView(generics.ListAPIView):
    serializer_class = MpesaCheckoutSerializer

    def get_queryset(self):
        queryset = Transaction.objects.all()
        timestamp = self.request.query_params.get('timestamp')
        if timestamp:
            queryset = Transaction.objects.filter(timestamp = timestamp)
        return queryset




class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = MpesaCheckoutSerializer

