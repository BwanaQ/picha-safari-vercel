from django.urls import path
from cart.views import index, add_to_cart, cart, checkout, remove_from_cart, paypal_process_payment, paypal_reverse, paypal_cancel
""",payment_checkout"""
urlpatterns = [
    path('', index, name='cart-home'),
    path('add_to_cart', add_to_cart, name='add'),
    path('remove_from_cart', remove_from_cart, name='remove'),
    path('cart', cart, name='cart'),

    path('checkout', checkout, name='checkout'),
    # path('payment', payment_checkout, name='payment'),
    path('payment/paypal', paypal_process_payment, name='paypal-process-payment'),
    path('payment/paypal-reverse', paypal_reverse, name='paypal-reverse'),
    path('payment/paypal-cancel', paypal_cancel, name='paypal-cancel'),

]