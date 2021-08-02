from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Course(models.Model):
    id_video = models.CharField(
        _("id video on youtube"), max_length=200, unique=True, primary_key=True)
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(_("description"))
    total_videos = models.IntegerField()
    authen = models.TextField()
    view = models.IntegerField()
