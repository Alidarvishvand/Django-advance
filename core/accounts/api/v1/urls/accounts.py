
from django.urls import path,include
from .. import views
#from rest_framework.authtoken.views import ObtainAuthToken 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    #regitration
    path('registeration/',views.RegisterationApiView.as_view(),name='registeration'),
    #activation 
    #resnd activation 
    #login
    path('token/login/',views.CustomObtainAuthToken.as_view(),name= 'login'),
    path('token/logout/',views.CUstomDiscardAuthToken.as_view(),name= 'logout'),
    #change-password
    path('password_change/',views.PasswordChangeApiView.as_view(),name='change-password'),
    #jwt
    path('jwt/create/',views.CustomTokenObtainPairView.as_view(),name= 'jwt-create'), 
    path('jwt/refresh/',TokenRefreshView.as_view(),name= 'jwt-refresh'), 
    path('jwt/verify/',TokenVerifyView.as_view(),name= 'jwt-verify'), 
]