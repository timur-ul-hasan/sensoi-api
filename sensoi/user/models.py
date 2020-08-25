from django.utils import timezone
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        print(email)
        try:
            tmp_user = self.model.objects.get(email=email)
            raise IntegrityError('User already exist with this email:%s' %
                                 email)
        except self.model.DoesNotExist as e:
            print(extra_fields)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


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
    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'