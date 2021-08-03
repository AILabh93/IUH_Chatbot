from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Course(models.Model):
    id_video = models.CharField(
        _("id video on youtube"), max_length=200, unique=True, primary_key=True)
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(_("description"))
    total_videos = models.PositiveSmallIntegerField()
    authen = models.CharField(max_length=200, blank=False)
    view = models.PositiveIntegerField()
    image = models.URLField(
        max_length=1000, default='https://iuhchatbot.xyz/course')
