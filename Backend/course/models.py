from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=200, blank=False)
    id_video = models.CharField(
        _("id video on youtube"), max_length=200, unique=True)
    description = models.TextField(_("description"))
    src = models.TextField(blank=True)
