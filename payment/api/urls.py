from rest_framework.authtoken.views import ObtainAuthToken, obtain_auth_token
from django.urls import path, include

from payment.api.views import *

urlpatterns = [
    path('checkout/', MpesaCheckoutView.as_view(), name='checkout'),
    path("callback/", MpesaCallBackView.as_view(), name="callback"),
    path('list/', PaymentListView.as_view(), name="payment-list"),
    path('<int:pk>/', PaymentDetailView.as_view(), name="payment-detail"),
]