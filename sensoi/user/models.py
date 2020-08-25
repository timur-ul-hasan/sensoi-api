from django.utils import timezone
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _

class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(
        _('email address'),
        blank=False,
        null=False,
        unique=True,
        error_messages={
            'unique': _("A project with that username already exists."),
        },
    )
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'