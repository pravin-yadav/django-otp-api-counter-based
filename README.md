# django-otp-api-counter-based

## API Calls

#### GET [Request OTP]
```http://127.0.0.1:8000/otp/${mobilenumber}/```

##### Response
Data: 
```
   {
    "OTP":040301,
    "isVerified": false
   }
```

#### POST [Verify OTP]
```http://127.0.0.1:8000/otp/${mobilenumber}/```

##### Response
Data: 
```
   {
    "message": "You are authorized",
    "isVerified": true
   }
```
