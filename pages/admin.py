from django.contrib import admin
from .models import Art, Blog, Project, ResumeEntry, Topic, BlogRollEntry

class ArtAdmin(admin.ModelAdmin):
    model = Art
    list_display = ["title", "image"]
admin.site.register(Art, ArtAdmin)

class BlogAdmin(admin.ModelAdmin):
    model = Blog
    list_display = ["title", "image"]
admin.site.register(Blog, BlogAdmin)

class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ["title", "image"]
admin.site.register(Project, ProjectAdmin)

class ResumeEntryAdmin(admin.ModelAdmin):
    model = ResumeEntry
    list_display = ["title", "company"]
admin.site.register(ResumeEntry, ResumeEntryAdmin)

class TopicAdmin(admin.ModelAdmin):
    model = Topic
    list_display = ["name"]
    list_display_links = ["name"]
admin.site.register(Topic, TopicAdmin)

class BlogRollEntryAdmin(admin.ModelAdmin):
    model = BlogRollEntry
    list_display = ["name"]
admin.site.register(BlogRollEntry, BlogRollEntryAdmin)
