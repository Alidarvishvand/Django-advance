from rest_framework import generics
from .serializers import (RegistrationSerializers,AuthTokenSerializer,
                         CustomTokenObtainPairSerializer,ChangePassword,ProfileSerializer)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from accounts.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework_simplejwt.views import TokenObtainPairView
from ...models import Profile
from django.shortcuts import get_object_or_404


# from django.core.mail import send_mail(send email with a terminal )

from mail_templated import send_mail






class RegisterationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializers
    
    def post(self,request,*args,**kwargs):
        
        serializer = RegistrationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data= {
                'email':serializer.validated_data['email']
            }
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class CustomObtainAuthToken(ObtainAuthToken):
        serializer_class = AuthTokenSerializer
        def post(self, request, *args, **kwargs):
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
             
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
            
class CUstomDiscardAuthToken(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self , request):
        request.user.auth_token.delet()
        return  Response(status=status.HTTP_204_NO_CONTENT)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class  = CustomTokenObtainPairSerializer
    
    
class PasswordChangeApiView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePassword
    def get_object(self,queryset=None):
        obj = self.request.user
        return obj
    
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({"old_password":["wrong password"]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.save()
            return Response({'details': 'password change successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer 
    queryset = Profile.objects.all()
    
    def get_object(self):
        queryset = self.queryset()
        obj = get_object_or_404(queryset,user=self.request.user)
        return obj
    

class TestEmailSend(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        send_mail('email/hello.tpl', {'name': 'ali'}, 'say@gmail.com', ['imalidrv@gmail.com'])

        return Response("email sents")