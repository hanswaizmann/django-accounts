from django.db import models

from django.contrib.auth.models import (
        BaseUserManager, AbstractUser
)
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from django.utils.text import slugify

from easy_thumbnails.fields import ThumbnailerImageField

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_('Email'), unique=True)
    password = models.CharField(_('Password'), max_length=128)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user          = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='userprofile')
    first_name    = models.CharField(_('First name'), default='', max_length=30)
    last_name     = models.CharField(_('Last name'), default='', max_length=30)
    www           = models.CharField(max_length=250, blank=True)
    bild          = ThumbnailerImageField(upload_to = 'profiles/', default = 'None/no_image.png')
    online        = models.BooleanField(default=False)
    desc          = models.TextField(default='', blank=True)

    def thumb(self):
        return format_html('<img src="{}" width="50px" height="50px" />'.format(self.bild['thumb100'].url))

    def thumb_medium(self):
        return format_html('<img src="{}" width="300px"  />'.format(self.bild['thumb300'].url))

    thumb.short_description = 'Image'
    thumb_medium.short_description = 'Image'

    def slug(self):
        return slugify(self.get_name(), allow_unicode=True)
    def get_name(self):
        return self.first_name + ' ' + self.last_name
    def get_absolute_url(self):
        return reverse('userprofile', args=(self.pk, self.slug(),))
    def __str__(self):
        return self.get_name()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
