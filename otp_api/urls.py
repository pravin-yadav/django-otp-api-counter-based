from django.urls import path, include
from .views import retriveAndVerifyOTP

urlpatterns = [
    path("<phone>/", retriveAndVerifyOTP.as_view(), name="OTP"),
]
