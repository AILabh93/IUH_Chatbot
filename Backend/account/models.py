from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.defaultfilters import truncatechars
# Create your models here.

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CustomUser(AbstractUser):

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    full_name = models.CharField(_('full name'), max_length=255, blank=False)
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(blank=True,
                               upload_to='avatars')

    @property
    def short_description(self):
        return truncatechars(self.full_name, 20)

    def user_photo(self):
        try:
            mark = mark_safe(
                '<img src = "{}" width = "40"/>'.format(self.avatar.url))
        except:
            mark = mark_safe(
                '<img src = "{}" width = "40"/>'.format('/media/avatars/default.jpg'))
        return mark

    user_photo.short_description = 'avatar'
    user_photo.allow_tags = True

    def __str__(self):
        return self.username
