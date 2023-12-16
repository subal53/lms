from django.shortcuts import render,HttpResponse
from django.conf import settings
from django.core.mail import send_mail
import random
# Create your views here.
def mail_ser(request):
    try:

        subject = 'LMS otp'
        otp = random.randint(111111,999999)
        message = f'Youer OTP is {otp}.\n Don\'t Share with anyone.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['subalpatra52@gmail.com' ]
        send_mail( subject, message, email_from, recipient_list )
        return HttpResponse(f'otp : {otp}')
    except:
        return HttpResponse("failed")