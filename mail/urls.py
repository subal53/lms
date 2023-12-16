from django.urls import path
from mail.views import *
urlpatterns = [
    path('send_mail', mail_ser, name='send mail'),
]
