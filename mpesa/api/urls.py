from django.urls import path
from mpesa.api.views import LNMCallbackUrlAPIView

urlpatterns = [
    path('lnm/', LNMCallbackUrlAPIView.as_view(), name="lnm-callback-url"),
] 