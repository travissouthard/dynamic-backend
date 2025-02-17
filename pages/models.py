import string
from django.db import models
from django.utils import timezone
from .helpers.posse import post_to_mastodon

class Post(models.Model):
    title = models.CharField(max_length=64)
    slug = models.CharField(max_length=64, null=True, blank=True, editable=False)
    site_link = models.URLField(max_length=2000, null=True, blank=True)
    code_link = models.URLField(max_length=2000, null=True, blank=True)
    description = models.TextField()
    alt_text = models.CharField(max_length=280, null=True, blank=True)
    published = models.DateField(default=timezone.now)
    last_updated = models.DateField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = "-".join([word.lower().strip(string.punctuation) for word in self.title.split(" ")])
            self.slug = slug
            post_to_mastodon(self)
        super(Post, self).save(*args, **kwargs)

class Art(Post):
    image = models.ImageField(upload_to="images/art/", null=True, blank=True)
    post_type = models.CharField(max_length=8, default="art")

class Blog(Post):
    image = models.ImageField(upload_to="images/blog/", null=True, blank=True)
    post_type = models.CharField(max_length=8, default="blog")

class Project(Post):
    image = models.ImageField(upload_to="images/projects/", null=True, blank=True)
    post_type = models.CharField(max_length=8, default="projects")

class ResumeEntry(models.Model):
    title = models.CharField(max_length=64)
    company = models.CharField(max_length=64)
    co_link = models.URLField(null=True, blank=True)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)

class Topic(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name

class BlogRollEntry(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField()
    topics = models.ManyToManyField(Topic)
