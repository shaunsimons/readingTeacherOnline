from django.contrib import admin
from .models import Blog, AboutMe, BlogImages

# Register your models here.


class BlogImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'url')

admin.site.register(Blog)
admin.site.register(BlogImages, BlogImageAdmin)
admin.site.register(AboutMe)