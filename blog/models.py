from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


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

    def __str__(self):
        return self.title

