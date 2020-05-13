from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import Q
from djongo import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, email, first_name, last_name):
        if self._credentials_already_in_use(username, email):
            raise ValueError('Username or email already in use.')

        user = User(username=username, email=email,
                    first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email, first_name, last_name):
        if self._credentials_already_in_use(username, email):
            raise ValueError('Username or email already in use.')

        user = User(username=username, email=email,
                    first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def _credentials_already_in_use(self, username, email):
        return User.objects.filter(Q(username=username),
                                   Q(email=email)).exists()


class User(AbstractBaseUser):
    username = models.CharField(max_length=16, null=False, blank=False,
                                unique=True, primary_key=True)
    email = models.CharField(max_length=255, null=False, blank=False,
                             unique=True)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    registration_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    objects = CustomUserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username
    
