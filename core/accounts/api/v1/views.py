from rest_framework import generics
from .serializers import (
    RegistrationSerializers,
    AuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePassword,
    ProfileSerializer,
    ActivationSerializer,
)
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
from ..utils import Emailthreading
from mail_templated import EmailMessage

# from django.core.mail import send_mail(send email with a terminal )

from mail_templated import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt import ExpiredSignatureError, InvalidSignatureError
from django.conf import settings


class RegisterationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializers

    def post(self, request, *args, **kwargs):

        serializer = RegistrationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {"email": email}

            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "say@gmail.com",
                to=[email],
            )
            Emailthreading(email_obj).start()

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {"token": token.key, "user_id": user.pk, "email": user.email}
        )


class CUstomDiscardAuthToken(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delet()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class PasswordChangeApiView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePassword

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(
                serializer.data.get("old_password")
            ):
                return Response(
                    {"old_password": ["wrong password"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.save()
            return Response(
                {"details": "password change successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class TestEmailSend(APIView):
    def post(self, request, *args, **kwargs):
        self.email = "imalidrv@gmail.com"
        user_obj = get_object_or_404(User, email=self.email)
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            "say@gmail.com",
            to=[self.email],
        )

        Emailthreading(email_obj).start()
        return Response("email sents")

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivateApiView(APIView):
    def get(self, request, token, *args, **kwargs):

        try:
            token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"details": "token is expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "token is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_obj = User.objects.get(pk=user_id)

        if user_obj.is_verified:
            return Response(
                {"details": "your account has alredy have been verified "},
                status=status.HTTP_200_OK,
            )
        user_obj.is_verified = True
        user_obj.save()

        return Response(
            {"details": "your account have been verified and activate"},
            status=status.HTTP_200_OK,
        )

        # decode - > id user
        # find object user
        # is_verifid - > True


class ResendActivationApiView(APIView):
    serilizer_class = ActivationSerializer

    def post(self, request, *args, **kwargs):

        serializer = ActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            "say@gmail.com",
            to=[user_obj.email],
        )
        Emailthreading(email_obj).start()
        return Response(
            {"detail": "user have been resend activation email successfully"},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
