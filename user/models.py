from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password 
from django.core.validators import MinLengthValidator



from .managers import UserManager



class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    password = models.CharField(_("password"),validators=[MinLengthValidator(8)], max_length=16)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
         verbose_name = "User"

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.pk and self.is_superuser == False:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)