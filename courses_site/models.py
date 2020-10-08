from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


STATUS = (
    (0, 'DRAFT'),
    (1, 'PUBLISHED')
)


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    status = models.IntegerField(choices=STATUS, default=0)
    slug = models.SlugField(default='', editable=False, max_length=200, null=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug
        }
        return reverse('course_detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class Video(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    free_to_watch = models.BooleanField(default=False)
    video_file = models.FileField(upload_to='course_site/courses/')

    class Meta:
        order_with_respect_to = 'course'

    def __str__(self):
        return self.title



class Watched(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    has_watched = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'watched'






