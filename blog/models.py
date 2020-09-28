from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify


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

