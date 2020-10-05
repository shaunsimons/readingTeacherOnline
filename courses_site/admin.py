from django.contrib import admin
from .models import Course, Video, Watched


class InlineVideo(admin.TabularInline):
    model = Video
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    inlines = [InlineVideo]

    class Media:
        css = {
            "all": ('courses_site/base.css',)
        }
        js = ('courses_site/my_code.js',)


admin.site.register(Course, CourseAdmin)
admin.site.register(Watched)
