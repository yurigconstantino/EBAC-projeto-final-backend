from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from django.contrib.auth import get_user_model

# Create your views here.
User = get_user_model()

class RegisterViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Usuario criado",
            "user": serializer.data
        }, status=status.HTTP_201_CREATED)
    
class LoginViewSet(APIView):

    def post(self, request):
        selializer = LoginSerializer(data=request.data)

        selializer.is_valid(raise_exception=True)

        return Response(selializer.validated_data, status=status.HTTP_200_OK)
    

class MeViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        serialiszer = UserSerializer(request.user)

        return Response(serialiszer.data)