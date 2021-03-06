from __future__ import unicode_literals
import os.path
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import (User,
										 BaseUserManager,
										 AbstractBaseUser, 
										 PermissionsMixin)
from django.utils.translation import ugettext_lazy as _
from local.constants import *
from django.conf import settings
from django.urls import reverse

# Create your models here.
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
        user = self.model(
            ID_Number=ID_Number, 
            **extra_fields
            )

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

    def get_by_natural_key(self, ID_Number):
        case_insensitive_ID_Number_field = '{}__iexact'.format(
            self.model.USERNAME_FIELD
            )

        return self.get(**{case_insensitive_ID_Number_field: ID_Number})


@python_2_unicode_compatible
class User(AbstractBaseUser, PermissionsMixin):
    ID_Number = models.CharField(
        max_length=15, 
        unique=True, 
        null=True
        )

    level = models.CharField(
        max_length=9,
        choices=LEVEL,
        )

    first_name = models.CharField(
        max_length=50, 
        blank=True, 
        null=True
        )

    last_name = models.CharField(
        max_length=50, 
        blank=True, 
        null=True
        )

    gender = models.CharField(
        _('Gender'),
        max_length=50, 
        blank=True,
        null=True,
        choices=GENDER,
        )

    hall_of_residence = models.CharField(
        _('Hall'),
        max_length=50, 
        choices=HALL_OF_RESIDENCE,
        blank=True, 
        null=True
        )

    state_of_origin = models.CharField(
        _('State'),
        max_length=50, 
        choices=STATES, 
        blank=True, 
        null=True
        )

    town = models.CharField(
        _('Local Government'),
        max_length=50, 
        choices=TOWNS,
        blank=True,
        null=True,
        )

    mobile = models.CharField(
        _('Phone'),
        max_length=11, 
        blank=True, 
        null=True
        )

    email = models.EmailField(
        _('Email'),
        help_text="e.g abcd@example.com",
        null=True,
        blank=True, 
        )

    facebook_id = models.CharField(
        _('Facebook'),
        help_text="Your facebook id e.g abdulrasheed.ibrahim.756",
    	max_length=50,
    	null=True,
    	blank=True
    	)
    twitter_handler = models.CharField(
        _('Twitter handler'),
        help_text="Your twitter handler e.g @abdulrasheed1",
    	max_length=50,
    	null=True,
    	blank=True
    	)
    instagram_id = models.CharField(
        _('Instagram'),
        help_text="Your instagram ID e.g abdoul_rasheed",
    	max_length=50,
    	null=True,
    	blank=True
    	)
    pinterest = models.CharField(
        _('Pinterest'),
        help_text = "Your pin ID e.g example",
    	max_length=50,
    	null=True,
    	blank=True
    	)


    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )


    is_staff = models.BooleanField(
		_('Site staff'),
        default=False,
        help_text=_('Designates whether the user can login to this site as admin.'),
    )


    is_d_staff = models.BooleanField(_('Department staff'),
        default=False,
        help_text=_('Designates whether the user is a Department staff.'),
        )

    is_student = models.BooleanField(
        _('is student'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active student. '
        ),
    )

    is_exco = models.BooleanField(
        _('Department exco'),
        default=False,
        help_text=_(
            'Designates whether this user should be displayed in the excos page. '
        ),
    )
    
    def __str__(self):
        return "%s" % self.user.ID_Number

    def get_url(self):
        url = self.url
        if "http://" not in self.url and "https://" not in self.url and len(self.url) > 0:  # noqa: E501
            url = "http://" + str(self.url)

        return url


    USERNAME_FIELD = 'ID_Number'

    REQUIRED_FIELDS = []
    
    objects = MyUserManager()

    class meta:
    	verbose_name = _('ID_Number')
    	verbose_name_plural = _('ID_Numbers')

    def __str__(self):
        return '%s' % self.ID_Number

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        if self.first_name and self.last_name:
            full_name = '%s %s' % (self.first_name, self.last_name)
            return full_name.strip()
        return self.ID_Number

    def get_short_name(self):
        "Returns the short name for the user."
        if self.first_name:
            return self.first_name
        return self.ID_Number

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.ID_Number)])


    def get_picture(self):
        no_picture = 'http://trybootcamp.vitorfs.com/static/img/user.png'
        try:
            filename = settings.MEDIA_ROOT + '/profile_pictures/' +\
                self.ID_Number + '.jpg'
            picture_url = settings.MEDIA_URL + 'profile_pictures/' +\
                self.ID_Number + '.jpg'
            if os.path.isfile(filename):  # pragma: no cover
                return picture_url
            else:  # pragma: no cover
                gravatar_url = 'http://www.gravatar.com/avatar/{0}?{1}'.format(
                    hashlib.md5(self.email.lower()).hexdigest(),
                    urllib.urlencode({'d': no_picture, 's': '256'})
                    )
                return gravatar_url

        except Exception:
            return no_picture

    def get_screen_name(self):
        try:
            if self.get_full_name():
                return self.get_full_name()

            else:
                return self.ID_Number

        except Exception:  # pragma: no cover
            return self.ID_Number

    def get_html_badge(self):
        ID_Number = escape(self.name)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % ('lightblue', name)
        if self.is_d_staff:
        	html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % ('#007bff', name)
        elif self.is_exco:
        	html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % ('green', name)
        return mark_safe(html)