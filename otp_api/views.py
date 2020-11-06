
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PhoneModel
import base64


# This class returns the string needed to generate the key
class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "randomhashedsecretKey"


class retriveAndVerifyOTP(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):
        try:
            # if Mobile already exists the take this else create New One
            mobile = PhoneModel.objects.get(mobile=phone)
        except ObjectDoesNotExist:
            PhoneModel.objects.create(
                mobile=phone,
            )
            mobile = PhoneModel.objects.get(
                mobile=phone)  # user Newly created Model
        mobile.counter += 1  # Update Counter At every Call
        mobile.isVerified = False
        mobile.save()  # Save the data
        keygen = generateKey()
        print("Keygen", keygen.returnValue(phone))
        key = base64.b32encode(keygen.returnValue(
            phone).encode())  # Key is generated
        OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        print(OTP.at(mobile.counter))
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        # Just for demonstration
        return Response({"OTP": OTP.at(mobile.counter)}, status=200)

    # OTP Verification
    @staticmethod
    def post(request, phone):
        try:
            mobile = PhoneModel.objects.get(mobile=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(
            phone).encode())  # Generating Key
        OTP = pyotp.HOTP(key)  # HOTP Model
        if OTP.verify(request.data["OTP"], mobile.counter):  # Verifying the OTP
            mobile.isVerified = True
            mobile.save()
            return Response({'message': 'You are authorised', 'isVerified': True}, status=200)
        return Response({'message': 'OTP is wrong'}, status=400)
