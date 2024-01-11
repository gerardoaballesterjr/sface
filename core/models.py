from django.contrib.auth.models import AbstractUser
from django.db import models
from django import urls
from core import utils

class User(AbstractUser):
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug
    
    def get_update_url(self):
        return urls.reverse_lazy('core:user:update', args=[self.slug])

    def get_delete_url(self):
        return urls.reverse_lazy('core:user:delete', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = utils.slug_generator(self) if not self.slug else self.slug
        return super().save(*args, **kwargs)

class Seminar(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seminar_user')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def get_update_url(self):
        return urls.reverse_lazy('core:seminar:update', args=[self.slug])

    def get_delete_url(self):
        return urls.reverse_lazy('core:seminar:delete', args=[self.slug])

    def get_detail_url(self):
        return urls.reverse_lazy('core:seminar:detail', args=[self.slug])
    
    def get_stream_url(self):
        return urls.reverse_lazy('core:seminar:stream', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = utils.slug_generator(self) if not self.slug else self.slug
        return super().save(*args, **kwargs)

class Statistic(models.Model):
    data = models.CharField(max_length=255)
    seminar = models.ForeignKey(Seminar, on_delete=models.CASCADE, related_name='seminar_statistic')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = utils.slug_generator(self) if not self.slug else self.slug
        return super().save(*args, **kwargs)