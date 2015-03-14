from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from .authenticators import QuietBasicAuthentication

class AuthView(APIView):
    authentication_classes = (QuietBasicAuthentication,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        login(request, request.user)
        return Response(self.serializer_class(request.user).data)

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response()
