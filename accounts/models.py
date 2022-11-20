import uuid
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .utils import generate_otp


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=11)


class OtpManager(models.Manager):

    def is_valid(self, request_id, phone_number, code):
        current_time = timezone.now()
        otp = Otp.objects.filter(request_id=request_id,
                                 otp_receiver=phone_number,
                                 code=code,
                                 created__lt=current_time,
                                 created__gt=current_time - timedelta(seconds=120),
                                 is_active=True).first()

        if otp:
            otp.is_active = False
            otp.save()
        else:
            print('Otp Dose not exist')
        return otp


class Otp(models.Model):
    request_id = models.UUIDField(editable=False, default=uuid.uuid4(), auto_created=True)
    otp_receiver = models.CharField(max_length=225, null=False, blank=False)
    code = models.CharField(max_length=6, default=generate_otp)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = OtpManager()

    def __str__(self):
        return self.otp_receiver
