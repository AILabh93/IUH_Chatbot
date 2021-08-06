from django.contrib import admin
from . import models

# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ['title', 'description']
    list_display = ('title', 'authen', 'total_videos', 'view',)


admin.site.register(models.Course, CourseAdmin)
