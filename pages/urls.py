from django.urls import path

from .views import home_view, about_view, projects_list_view, art_list_view, blog_list_view, webring_view, resume_view, rss_view, redirect_old_html_links

urlpatterns = [
    path("<str:route>.html", redirect_old_html_links, name="html_links"),
    path("", home_view, name="home"),
    path("index", home_view, name="home"),
    path("about", about_view, name="about"),
    path("resume", resume_view, name="resume"),
    path("webring", webring_view, name="webring"),
    path("rss", rss_view, name="rss"),
    path("rss.xml", rss_view, name="rss"),
    path("projects", project_list_view, name="projects"),
    path("art", art_list_view, name="art"),
    path("blog", blog_list_view, name="blog")
]