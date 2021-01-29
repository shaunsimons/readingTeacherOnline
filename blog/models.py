from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import re



STATUS = (
    (0, 'DRAFT'),
    (1, 'PUBLISHED')
)


class BlogImages(models.Model):
    img_title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='blog/images')
    url = models.URLField(default='', blank=True, editable=False)

    def __str__(self):
        return self.img_title

    def save(self, *args, **kwargs):
        img_url = self.image.url
        base_url = img_url.split("?")[0]
        self.url = base_url
        super().save(*args, **kwargs)





class Blog(models.Model):
    title = models.CharField(max_length=200, unique=True)
    # content = RichTextUploadingField(blank=True, null=True)
    content = models.FileField(default=None, null=True)
    content_parsed = models.TextField(default='', blank=True)
    main_image = models.ImageField(upload_to='blog/images', default='blog/images/readingwithkids.jpg')
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    slug = models.SlugField(default='', editable=False, max_length=200, null=False)

    def get_parsed_content(self):
        read_content = self.content.read().decode("utf-8").replace("\n", " ").replace("\t", " ")
        pattern = re.compile("(?:<body.*?>)(.*)(?:</body>)")
        content = pattern.findall(read_content)[0]
        return content

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

        self.content_parsed = self.get_parsed_content()

        super().save(*args, **kwargs)





def validate_only_one_instance(obj):
    model = obj.__class__
    if model.objects.count() > 0 and obj.id not in model.objects.values_list('id', flat=True):
        raise ValidationError(f"Can only create 1 {model.__name__} instance")


class AboutMe(models.Model):
    thumbnail = models.ImageField()
    description = models.TextField()

    def clean(self):
        validate_only_one_instance(self)

