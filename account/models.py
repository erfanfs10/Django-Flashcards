from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from .manager import UserManager
from .tasks import send_welcome_email_task


class User(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email
    
    def send_email(self, subject, message):
        from_email = settings.EMAIL_HOST_USER
        to = (self.email,)
        send_welcome_email_task.apply_async(
            args=[subject, message, from_email, to],
             ignore_result=True)

    def send_sms(self):
        pass
    