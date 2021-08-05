from django.contrib import admin
from . import models

# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    # exclude = ('slug', )
    list_display = ('title', 'authen', 'total_videos', 'view',)


admin.site.register(models.Course, CourseAdmin)
