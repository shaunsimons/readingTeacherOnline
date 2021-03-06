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
    description = models.TextField(max_length=500)
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
    length = models.DurationField()
    activity_pdf = models.FileField(null=True, blank=True)

    class Meta:
        order_with_respect_to = 'course'

    def __str__(self):
        return self.title

    def length_formatter(self):
        """
            Convert length timedelta to MM:SS string format.
        """
        total = int(self.length.total_seconds())
        minutes = total // 60 if len(str(int(total // 60))) > 1 else f'0{total // 60}'
        seconds = total % 60 if len(str(int(total % 60))) > 1 else f'0{total % 60}'
        return f'{minutes}:{seconds}'


class Watched(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    has_watched = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'watched'





