from django.core.mail import send_mail
import random
from django.conf import settings
from .models import CustomUser

def email_otp(email):
    subject = "Your email is verified"
    otp = random.randint(1000, 9999)
    message = f"your otp is {otp}"
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email] )
    CustomUser_obj = CustomUser.objects.get(email=email)
    CustomUser_obj.otp = otp
    CustomUser_obj.save()