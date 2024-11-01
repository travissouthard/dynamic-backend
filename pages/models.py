from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=64)
    slug = models.CharField()
    site_link = models.URLField(max_length=2000, null=True)
    code_link = models.URLField(max_length=2000, null=True)
    description = models.TextField()
    alt_text = models.CharField(null=True)
    published = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        slug = self.title.lower().split(" ")
        self.slug = "-".join(slug)
        super(Post, self).save(*args, **kwargs)

class Art(Post):
    image = models.ImageField(upload_to="art/", null=True)

class Blog(Post):
    image = models.ImageField(upload_to="blog/", null=True)

class Project(Post):
    image = models.ImageField(upload_to="projects/", null=True)

class ResumeEntry(models.Model):
    title = models.CharField()
    company = models.CharField()
    co_link = models.URLField(null=True)
    start = models.DateField()
    end = models.DateField()
    location = models.CharField()
    description = models.TextField(null=True)

class Topic(models.Model):
    name = models.CharField(max_length=16, unique=True)

class BlogRollEntry(models.Model):
    name = models.CharField()
    link = models.URLField()
    topics = models.ManyToManyField(Topic)
