from django.contrib import admin
from .models import Course, Video, Watched


class InlineVideo(admin.TabularInline):
    model = Video
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    inlines = [InlineVideo]


admin.site.register(Course, CourseAdmin)
admin.site.register(Watched)
