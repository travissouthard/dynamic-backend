from django.urls import path

from .views import home_view, about_view, projects_view, art_view, blog_view, webring_view, resume_view, rss_view, redirect_old_html_links

urlpatterns = [
    path("<str:route>.html", redirect_old_html_links, name="html_links"),
    path("", home_view, name="home"),
    path("about", about_view, name="about"),
    path("resume", resume_view, name="resume"),
    path("webring", webring_view, name="webring"),
    path("rss", rss_view, name="rss"),
    path("rss.xml", rss_view, name="rss"),
    path("projects", projects_view, name="projects"),
    path("art", art_view, name="art"),
    path("blog", blog_view, name="blog")
]