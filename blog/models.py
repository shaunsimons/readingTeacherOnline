from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.core.exceptions import ValidationError


STATUS = (
    (0, 'DRAFT'),
    (1, 'PUBLISHED')
)


class Blog(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = RichTextUploadingField(blank=True, null=True)
    main_image = models.ImageField(upload_to='blog/images', default='blog/images/readingwithkids.jpg')
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    slug = models.SlugField(default='', editable=False, max_length=200, null=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('blog:blog_detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


def validate_only_one_instance(obj):
    model = obj.__class__
    if model.objects.count() > 0 and obj.id not in model.objects.values_list('id', flat=True):
        raise ValidationError(f"Can only create 1 {model.__name__} instance")


class AboutMe(models.Model):
    thumbnail = models.ImageField()
    description = models.TextField(max_length=1000)

    def clean(self):
        validate_only_one_instance(self)

