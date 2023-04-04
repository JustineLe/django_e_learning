from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class MyAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):

        user = self.model(
            email=self.normalize_email(email).lower(),
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = MyAccountManager()

    def __str__(self):
        return self.email
