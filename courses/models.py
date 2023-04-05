from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from courses.fields import OrderField


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    class Meta:
        ordering = ['-created']

    owner = models.ForeignKey(User,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    class Meta:
        ordering = ['order']

    course = models.ForeignKey(Course,
                               related_name='models',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'], default=0)  # ordering calc with respect to course (sequence number)

    def __str__(self):
        return f'{self.order}. {self.title}'


class Content(models.Model):
    class Meta:
        ordering = ['order']

    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': ('text', 'video', 'image', 'file')})
    object_id = models.PositiveIntegerField()  # target object id
    item = GenericForeignKey('content_type', 'object_id')  # target as relationship
    order = OrderField(blank=True, for_fields=['module'], default=1)  # sequence number in module


class ItemBase(models.Model):
    owner = models.ForeignKey(User,
                              related_name="%(class)s_related",  # text_related, file_related, video_related etc.
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(
        upload_to='images')  # https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.FileField.upload_to


class Video(ItemBase):
    url = models.URLField()
