from mpesa.models import LNMOnline
from mpesa.api.serializers import LNMOnlineSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

class LNMCallbackUrlAPIView(CreateAPIView):
    queryset = LNMOnline.objects.all()
    serializer_class = LNMOnlineSerializer
    permission_classes = [AllowAny]

    def create(self,request):
        print(request.data,"This is request.data")