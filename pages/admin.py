from django.contrib import admin
from .models import Art, Blog, Project, ResumeEntry, Topic, BlogRollEntry

# Example for custom Admins
# class AuthorAdmin(admin.ModelAdmin):
#     pass

# admin.site.register(Author, AuthorAdmin)

admin.site.register(Art)
admin.site.register(Blog)
admin.site.register(Project)
admin.site.register(ResumeEntry)
admin.site.register(Topic)
admin.site.register(BlogRollEntry)
