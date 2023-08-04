from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.core.mail import send_mail
from authentication import settings


@shared_task()
def send_register_mail(data, otp):

    mail_subject = "OTP Code"
    message = f"Your OTP code is {otp}.\n" \
                f"To verify please use this code."
    recipient_list = [data['otp_receiver']]

    send_mail(
        subject = mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
        )
    
    return "Done"