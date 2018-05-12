#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from django.core.urlresolvers import reverse

# rename image while upload
import os
from uuid import uuid4

class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with ID_Numbers as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, ID_Number, password, **extra_fields):
        """
        Creates and saves a User with the given ID_Number and password.
        """
        if not ID_Number:
            raise ValueError("Student ID Number can't be empty")
        ID_Number = self.normalize_email(ID_Number)
        user = self.model(ID_Number=ID_Number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, ID_Number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(ID_Number, password, **extra_fields)

# rename uploaded images
def path_and_rename(instance, filename):
    upload_to = 'profile_pictures'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        num_digits = 10
        # generate random number and append it to student ID_Number
        ins = instance.ID_Number + "-"+ hex(100*(instance.id + 123456789))
        filename = '{}.{}'.format(str(ins), ext)
    else:
        # set profile_picture name as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        filename.lower()
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class User(AbstractBaseUser, PermissionsMixin):
    ID_Number = models.CharField(max_length=12, unique=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    level = models.PositiveIntegerField(default=0)
    hall_of_residence = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=path_and_rename,
     blank=True,
     null=True,
     help_text="499 x 499 pixels recommnded",
     default = "no_image/default_user_image.png",
     )
    updated_at = models.DateTimeField(auto_now_add=True)
    is_updated = models.BooleanField(default=False)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = 'ID_Number'

    REQUIRED_FIELDS = ['level']
    
    objects = MyUserManager()

    def __str__(self):
        return str(self.ID_Number)

    def get_full_name(self):
        return self.ID_Number

    def get_short_name(self):
        return self.ID_Number

    def get_absolute_url(self):
      return reverse('profile', args=[str(self.id)])


class Office(models.Model):
    office = models.CharField(max_length=200)

    def __str__(self):  # Python 3: def __str__(self):
        return self.office

class Aspirant(models.Model):
    aspiring_for = models.ForeignKey(Office)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    nick_name = models.CharField(max_length=50, blank=True, null=True)
    level = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)


    def __str__(self):  # Python 3: def __str__(self):
        return self.first_name + " " + str(self.last_name)


class Voter(models.Model):
    student = models.ForeignKey(User)
    office = models.ForeignKey(Office)
    def __str__(self):
        if self.student.first_name and self.student.last_name:
            return str(self.student) + " (" + self.student.first_name + " " + self.student.last_name + ")"
        else:
            return str(self.student)