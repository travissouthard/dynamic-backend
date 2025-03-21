# Generated by Django 5.1.2 on 2024-11-03 02:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Art",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=64)),
                (
                    "slug",
                    models.CharField(
                        blank=True, editable=False, max_length=64, null=True
                    ),
                ),
                ("site_link", models.URLField(blank=True, max_length=2000, null=True)),
                ("code_link", models.URLField(blank=True, max_length=2000, null=True)),
                ("description", models.TextField()),
                ("alt_text", models.CharField(blank=True, max_length=280, null=True)),
                ("published", models.DateField(default=django.utils.timezone.now)),
                ("last_updated", models.DateField(auto_now=True)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="images/art/"),
                ),
                ("post_type", models.CharField(default="art", max_length=8)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=64)),
                (
                    "slug",
                    models.CharField(
                        blank=True, editable=False, max_length=64, null=True
                    ),
                ),
                ("site_link", models.URLField(blank=True, max_length=2000, null=True)),
                ("code_link", models.URLField(blank=True, max_length=2000, null=True)),
                ("description", models.TextField()),
                ("alt_text", models.CharField(blank=True, max_length=280, null=True)),
                ("published", models.DateField(default=django.utils.timezone.now)),
                ("last_updated", models.DateField(auto_now=True)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="images/blog/"),
                ),
                ("post_type", models.CharField(default="blog", max_length=8)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=64)),
                (
                    "slug",
                    models.CharField(
                        blank=True, editable=False, max_length=64, null=True
                    ),
                ),
                ("site_link", models.URLField(blank=True, max_length=2000, null=True)),
                ("code_link", models.URLField(blank=True, max_length=2000, null=True)),
                ("description", models.TextField()),
                ("alt_text", models.CharField(blank=True, max_length=280, null=True)),
                ("published", models.DateField(default=django.utils.timezone.now)),
                ("last_updated", models.DateField(auto_now=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="images/project/"
                    ),
                ),
                ("post_type", models.CharField(default="project", max_length=8)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ResumeEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=64)),
                ("company", models.CharField(max_length=64)),
                ("co_link", models.URLField(blank=True, null=True)),
                ("start", models.DateField()),
                ("end", models.DateField()),
                ("location", models.CharField(max_length=32)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Topic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=16, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="BlogRollEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("link", models.URLField()),
                ("topics", models.ManyToManyField(to="pages.topic")),
            ],
        ),
    ]
